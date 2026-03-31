import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
import json
import os
from datetime import datetime, date
from urllib3.exceptions import InsecureRequestWarning

# 设置编码
import sys
sys.stdout.reconfigure(encoding='utf-8')

# 忽略HTTPS证书警告
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# -------------------------- 新增：每日更新配置 --------------------------
# 存储最后更新信息的文件（用于判断是否需要爬取当日数据）
UPDATE_RECORD_PATH = "last_update_record.json"
# 爬取结果的基础保存路径（按日期命名，避免覆盖）
BASE_SAVE_DIR = "中药价格数据"

# -------------------------- 原有配置保留并优化 --------------------------
# 增强版请求头（随机User-Agent池，进一步降低反爬概率）
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
]
# 基础URL
BASE_URL = "https://www.kmzyw.com.cn/jiage/today_price.html?pageNum={}"

# ===== 核心防反爬参数（低速版）=====
EMPTY_PAGE_THRESHOLD = 2  # 连续2页无数据停止（你要改的）
REQUEST_TIMEOUT = 20
MIN_DELAY = 3
MAX_DELAY = 6
BATCH_SIZE = 10
BATCH_REST_MIN = 10
BATCH_REST_MAX = 20
MAX_RETRY = 2  # 单页失败重试2次（你要改的）


# -------------------------- 新增：每日更新校验函数 --------------------------
def get_random_headers():
    """新增：随机生成请求头，替换原有固定HEADERS"""
    headers = {
        "User-Agent": random.choice(USER_AGENTS),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "Accept-Encoding": "gzip, deflate, br",
        "Referer": "https://www.kmzyw.com.cn/",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-User": "?1",
        "Cache-Control": "max-age=0"
    }
    return headers


def get_last_update_info():
    """获取最后一次更新的记录（日期+文件路径）"""
    if not os.path.exists(UPDATE_RECORD_PATH):
        return {"last_update_date": "", "save_path": ""}
    try:
        with open(UPDATE_RECORD_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"⚠️ 读取更新记录失败：{e}，将重新爬取")
        return {"last_update_date": "", "save_path": ""}


def need_update_today():
    """判断是否需要更新今日数据"""
    last_info = get_last_update_info()
    last_date = last_info.get("last_update_date", "")
    today_str = date.today().strftime("%Y-%m-%d")

    # 无记录 或 最后更新日期不是今天 → 需要更新
    if not last_date or last_date != today_str:
        print(f"✅ 今日（{today_str}）未更新数据，开始执行爬取任务")
        return True
    else:
        print(f"ℹ️ 今日（{today_str}）数据已更新，无需重复爬取")
        print(f"   上次更新文件路径：{last_info.get('save_path', '未知')}")
        return False


def save_update_record(save_path):
    """保存本次更新的记录（日期+文件路径）"""
    try:
        record = {
            "last_update_date": date.today().strftime("%Y-%m-%d"),
            "save_path": save_path,
            "update_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        with open(UPDATE_RECORD_PATH, "w", encoding="utf-8") as f:
            json.dump(record, f, ensure_ascii=False, indent=2)
        print(f"✅ 更新记录已保存：{UPDATE_RECORD_PATH}")
    except Exception as e:
        print(f"⚠️ 保存更新记录失败：{e}")


# -------------------------- 原有函数优化（适配新逻辑） --------------------------
def random_sleep():
    """生成随机延时（模拟人类操作的非固定间隔）"""
    sleep_time = random.uniform(MIN_DELAY, MAX_DELAY)
    print(f"【防反爬】随机延时 {sleep_time:.2f} 秒...")
    time.sleep(sleep_time)


def batch_rest(page_num):
    """每爬完指定批次页数，额外休息一段时间"""
    if page_num % BATCH_SIZE == 0 and page_num > 0:
        rest_time = random.uniform(BATCH_REST_MIN, BATCH_REST_MAX)
        print(f"\n【批次休息】已爬{page_num}页，额外休息 {rest_time:.2f} 秒...")
        time.sleep(rest_time)


def parse_single_page(page_num):
    """解析单页数据（增加重试和容错，替换为随机请求头）"""
    page_data = []
    retry_count = 0

    while retry_count < MAX_RETRY:
        try:
            current_url = BASE_URL.format(page_num)
            print(f"\n===== 开始爬取第{page_num}页 ===== URL: {current_url}")

            # 发送请求（使用随机请求头，关闭连接复用）
            response = requests.get(
                url=current_url,
                headers=get_random_headers(),
                verify=False,
                timeout=REQUEST_TIMEOUT,
                stream=False,
                allow_redirects=True
            )
            response.raise_for_status()
            response.encoding = response.apparent_encoding or "utf-8"
            soup = BeautifulSoup(response.text, "html.parser")

            # 定位表格
            table = soup.find("table") or soup.find("div", class_="table")
            if not table:
                print(f"第{page_num}页：未找到数据表格")
                break

            rows = table.find_all("tr")[1:]
            if not rows:
                print(f"第{page_num}页：无数据行")
                break

            # 解析数据
            for row in rows:
                cols = row.find_all("td")
                if len(cols) < 9:
                    continue
                item = {
                    "品名": cols[0].text.strip(),
                    "规格": cols[1].text.strip(),
                    "产地": cols[2].text.strip(),
                    "亳州价格": cols[3].text.strip().replace("--", "无"),
                    "安国价格": cols[4].text.strip().replace("--", "无"),
                    "成都价格": cols[5].text.strip().replace("--", "无"),
                    "玉林价格": cols[6].text.strip().replace("--", "无"),
                    "廉桥价格": cols[7].text.strip().replace("--", "无"),
                    "普宁价格": cols[8].text.strip().replace("--", "无"),
                    "爬取页码": page_num,
                    "爬取时间": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                page_data.append(item)

            print(f"第{page_num}页：成功解析 {len(page_data)} 条数据")
            break

        except requests.exceptions.RequestException as e:
            retry_count += 1
            error_type = type(e).__name__
            print(f"第{page_num}页：请求失败（{error_type}），重试 {retry_count}/{MAX_RETRY} → {str(e)[:60]}")
            if retry_count < MAX_RETRY:
                time.sleep(random.uniform(MAX_DELAY, MAX_DELAY + 3))
        except Exception as e:
            print(f"第{page_num}页：解析异常 → {str(e)[:60]}")
            break

    random_sleep()
    batch_rest(page_num)
    return page_data


def crawl_all_pages():
    """无上限爬取所有页面（低速版）"""
    all_data = []
    current_page = 1
    empty_page_count = 0

    print("\n===== 低速防反爬模式启动 =====\n")
    print(f"爬取规则：")
    print(f"- 每页延时 {MIN_DELAY}~{MAX_DELAY} 秒")
    print(f"- 每{BATCH_SIZE}页休息 {BATCH_REST_MIN}~{BATCH_REST_MAX} 秒")
    print(f"- 连续{EMPTY_PAGE_THRESHOLD}页无数据自动停止\n")

    while True:
        page_data = parse_single_page(current_page)

        if len(page_data) == 0:
            empty_page_count += 1
            print(f"第{current_page}页：无有效数据 | 连续无数据：{empty_page_count}/{EMPTY_PAGE_THRESHOLD}")
            if empty_page_count >= EMPTY_PAGE_THRESHOLD:
                print(f"\n✅ 连续{EMPTY_PAGE_THRESHOLD}页无数据，判定爬取完成，停止任务")
                break
        else:
            empty_page_count = 0
            all_data.extend(page_data)

        current_page += 1

    return all_data


def save_data_to_excel(data):
    """保存数据到Excel"""
    if not data:
        print("\n❌ 无任何数据可保存")
        return ""

    try:
        if not os.path.exists(BASE_SAVE_DIR):
            os.makedirs(BASE_SAVE_DIR)

        df = pd.DataFrame(data)
        df = df.drop_duplicates(subset=["品名", "规格", "产地"], keep="first")
        df = df.sort_values(by=["爬取页码", "品名"])

        today_str = date.today().strftime("%Y%m%d")
        save_path = os.path.join(BASE_SAVE_DIR, f"康美中药网价格_{today_str}.xlsx")
        df.to_excel(save_path, index=False, engine="openpyxl")

        save_update_record(save_path)

        print("\n" + "=" * 60)
        print(f"✅ 数据保存成功！")
        print(f"- 原始爬取条数：{len(data)}")
        print(f"- 去重后条数：{len(df)}")
        print(f"- 保存路径：{save_path}")
        print("=" * 60)
        return save_path
    except Exception as e:
        print(f"\n❌ 数据保存失败 → {str(e)}")
        return ""


def main():
    """主逻辑：校验是否需要更新 → 爬取 → 保存"""
    print("===== 康美中药网价格爬取系统启动 =====\n")

    if not need_update_today():
        return

    total_data = []
    try:
        total_data = crawl_all_pages()
    except KeyboardInterrupt:
        print("\n\n⚠️ 用户手动终止爬取！正在保存已爬取的数据...")
    except Exception as e:
        print(f"\n❌ 爬取过程出现致命错误 → {str(e)}")

    save_data_to_excel(total_data)
    print("\n===== 爬取任务执行完毕 =====\n")


if __name__ == "__main__":
    main()