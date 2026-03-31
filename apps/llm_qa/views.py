"""LLM QA views."""

from django.shortcuts import render, redirect
from .forms import QuestionForm
from .models import QuestionAnswer
from .utils.llm_client import get_llm_response


def ask_question(request):
    """Ask question view."""
    answer = None
    chat_history = []
    
    if request.method == 'POST':
        # 检查是否直接提交了question字段（来自提示词按钮）
        if 'question' in request.POST:
            question = request.POST['question']
            form = QuestionForm(request.POST)
        else:
            form = QuestionForm(request.POST)
            if form.is_valid():
                question = form.cleaned_data['question']
            else:
                question = None
        
        if question:
            conversation_history = request.session.get('conversation_history', [])
            
            answer = get_llm_response(question, conversation_history)
            
            conversation_history.append({"role": "user", "content": question})
            conversation_history.append({"role": "assistant", "content": answer})
            
            request.session['conversation_history'] = conversation_history[-10:]
            
            chat_history = []
            for i in range(0, len(conversation_history), 2):
                if i + 1 < len(conversation_history):
                    chat_history.append({
                        'question': conversation_history[i]['content'],
                        'answer': conversation_history[i + 1]['content']
                    })
            
            qa_record = QuestionAnswer(question=question)
            if request.user.is_authenticated:
                qa_record.user = request.user
            qa_record.answer = answer
            qa_record.model_used = 'GLM-4.7-Flash'
            qa_record.save()
    else:
        form = QuestionForm()
        # 保持现有对话历史，不重置
        conversation_history = request.session.get('conversation_history', [])
        chat_history = []
        for i in range(0, len(conversation_history), 2):
            if i + 1 < len(conversation_history):
                chat_history.append({
                    'question': conversation_history[i]['content'],
                    'answer': conversation_history[i + 1]['content']
                })
    
    return render(request, 'llm_qa/ask.html', {
        'form': form,
        'answer': answer,
        'chat_history': chat_history
    })


def clear_history(request):
    """Clear conversation history."""
    if request.method == 'POST':
        request.session['conversation_history'] = []
    return redirect('llm_qa:ask_question')


def delete_history(request):
    """Delete specific conversation from history."""
    if request.method == 'POST':
        try:
            index = int(request.POST.get('index', -1))
            if index >= 0:
                conversation_history = request.session.get('conversation_history', [])
                # 每个对话包含2条消息（问题和回答）
                start_idx = index * 2
                end_idx = start_idx + 2
                if start_idx < len(conversation_history):
                    del conversation_history[start_idx:end_idx]
                    request.session['conversation_history'] = conversation_history
        except ValueError:
            pass
    return redirect('llm_qa:ask_question')
