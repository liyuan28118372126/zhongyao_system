// 中药系统 - 主要JavaScript文件 - v2.0

document.addEventListener('DOMContentLoaded', function() {
    // 初始化所有工具提示
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // 初始化所有弹出框
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // 搜索框焦点效果
    const searchInputs = document.querySelectorAll('.header-search input, .hero-search input');
    searchInputs.forEach(input => {
        input.addEventListener('focus', function() {
            this.closest('.input-group').style.boxShadow = '0 4px 20px rgba(40, 167, 69, 0.3)';
        });
        
        input.addEventListener('blur', function() {
            this.closest('.input-group').style.boxShadow = '';
        });
    });

    // 分类卡片悬停效果
    const categoryCards = document.querySelectorAll('.category-card');
    categoryCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-8px)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });

    // 导航栏滚动效果
    let lastScrollTop = 0;
    const navbar = document.querySelector('.navbar');
    
    window.addEventListener('scroll', function() {
        let scrollTop = window.pageYOffset || document.documentElement.scrollTop;
        
        if (scrollTop > lastScrollTop && scrollTop > 100) {
            // 向下滚动
            navbar.style.transform = 'translateY(-100%)';
        } else {
            // 向上滚动
            navbar.style.transform = 'translateY(0)';
        }
        
        lastScrollTop = scrollTop;
    });

    // 添加页面加载动画
    const animatedElements = document.querySelectorAll('.category-card, .card');
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px 0px 0px'
    };

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in-up');
                entry.target.style.opacity = '1';
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    animatedElements.forEach(el => {
        // 先检查元素是否已经在视口中
        const rect = el.getBoundingClientRect();
        const isInViewport = (
            rect.top >= 0 &&
            rect.left >= 0 &&
            rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
            rect.right <= (window.innerWidth || document.documentElement.clientWidth)
        );
        
        if (isInViewport) {
            el.classList.add('fade-in-up');
            el.style.opacity = '1';
        } else {
            el.style.opacity = '0';
            observer.observe(el);
        }
    });

    // 搜索建议功能（简单实现）
    const searchInput = document.querySelector('.hero-search input[name="q"]');
    if (searchInput) {
        const suggestions = ['人参', '当归', '黄芪', '枸杞', '甘草', '白术', '茯苓', '川芎'];
        
        searchInput.addEventListener('input', function() {
            const value = this.value.toLowerCase();
            // 这里可以添加更复杂的搜索建议逻辑
        });
    }

    // 登录模态框功能
    const salesLink = document.getElementById('sales-link');
    if (salesLink) {
        salesLink.addEventListener('click', function(e) {
            // 检查用户是否已登录
            const authStatusElement = document.getElementById('user-auth-status');
            const isLoggedIn = authStatusElement && authStatusElement.getAttribute('data-authenticated') === 'true';
            
            if (!isLoggedIn) {
                e.preventDefault();
                // 显示登录模态框
                const loginModal = new bootstrap.Modal(document.getElementById('loginModal'));
                loginModal.show();
                // 设置登录后的跳转地址
                document.getElementById('login-next').value = this.getAttribute('href');
            }
        });
    }

    console.log('中药系统已加载完成');
});

// 表单验证辅助函数
function validateForm(formId) {
    const form = document.getElementById(formId);
    if (!form) return true;

    const requiredFields = form.querySelectorAll('[required]');
    let isValid = true;

    requiredFields.forEach(field => {
        if (!field.value.trim()) {
            field.classList.add('is-invalid');
            isValid = false;
        } else {
            field.classList.remove('is-invalid');
        }
    });

    return isValid;
}

// 图片预览功能
function previewImage(input, previewId) {
    const preview = document.getElementById(previewId);
    if (input.files && input.files[0]) {
        const reader = new FileReader();
        reader.onload = function(e) {
            preview.src = e.target.result;
            preview.style.display = 'block';
        };
        reader.readAsDataURL(input.files[0]);
    }
}

// 确认删除功能
function confirmDelete(message) {
    return confirm(message || '确定要删除这个项目吗？此操作不可撤销。');
}

// 返回顶部功能
function scrollToTop() {
    window.scrollTo({
        top: 0,
        behavior: 'smooth'
    });
}

// 添加返回顶部按钮
window.addEventListener('scroll', function() {
    const backToTopBtn = document.getElementById('back-to-top');
    if (backToTopBtn) {
        if (window.pageYOffset > 300) {
            backToTopBtn.style.display = 'block';
        } else {
            backToTopBtn.style.display = 'none';
        }
    }
});