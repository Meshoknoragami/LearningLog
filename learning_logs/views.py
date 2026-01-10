from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.db.models import Count, Max

from .models import Topic, Entry
from .forms import TopicForm, EntryForm

import json
from django.http import JsonResponse
from django.http import HttpResponse
from django.utils.text import slugify
from django.contrib import messages
from datetime import datetime

from django.contrib.contenttypes.models import ContentType
from .models import Bookmark


def index(request):
    """Домашняя страница представления Learning Log"""
    return render(request, 'learning_logs/index.html')


@login_required
def topics(request):
    topics = Topic.objects.filter(owner=request.user).annotate(
        entries_count=Count('entry'),
        last_entry_date=Max('entry__date_added')
    ).order_by('date_added')

    # Проверяем закладки
    topic_ids = [t.id for t in topics]
    topic_type = ContentType.objects.get_for_model(Topic)
    bookmarked_topic_ids = Bookmark.objects.filter(
        user=request.user,
        content_type=topic_type,
        object_id__in=topic_ids
    ).values_list('object_id', flat=True)

    # Добавляем флаг
    for topic in topics:
        topic.is_bookmarked = topic.id in bookmarked_topic_ids

    return render(request, 'learning_logs/topics.html', {'topics': topics})


@login_required
def topic(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id, owner=request.user)
    entries = topic.entry_set.order_by('-date_added')

    # Закладки для записей
    entry_ids = [e.id for e in entries]
    entry_type = ContentType.objects.get_for_model(Entry)
    bookmarked_entry_ids = Bookmark.objects.filter(
        user=request.user,
        content_type=entry_type,
        object_id__in=entry_ids
    ).values_list('object_id', flat=True)

    for entry in entries:
        entry.is_bookmarked = entry.id in bookmarked_entry_ids

    context = {'topic': topic, 'entries': entries}
    return render(request, 'learning_logs/topic.html', context)


@login_required
def new_topic(request):
    if request.method == 'POST':
        # Определяем: это импорт или обычная форма?
        if request.FILES.get('topic_file'):
            topic_file = request.FILES['topic_file']
            try:
                data = json.load(topic_file)
                topic_name = data.get('topic_name')
                entries = data.get('entries', [])

                if not topic_name:
                    messages.error(request, "Invalid file: missing 'topic_name'.")
                    return render(request, 'learning_logs/new_topic.html')

                topic = Topic(owner=request.user, text=topic_name)
                topic.save()

                for entry_data in entries:
                    text = entry_data.get('text', '')
                    date_str = entry_data.get('date_added')
                    entry = Entry(topic=topic, text=text)
                    if date_str:
                        try:
                            # Обработка даты (может быть с часовым поясом)
                            entry.date_added = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
                        except:
                            pass
                    entry.save()

                messages.success(request, f"Topic '{topic_name}' imported!")
                return redirect('learning_logs:topic', topic_id=topic.id)

            except Exception as e:
                messages.error(request, "Error importing file. Please check format.")
                return render(request, 'learning_logs/new_topic.html')

        else:
            # Обычная форма
            form = TopicForm(data=request.POST)
            if form.is_valid():
                new_topic = form.save(commit=False)
                new_topic.owner = request.user
                new_topic.save()
                return redirect('learning_logs:topics')
            else:
                return render(request, 'learning_logs/new_topic.html', {'form': form})

    else:
        return render(request, 'learning_logs/new_topic.html', {'form': TopicForm()})


@login_required
def new_entry(request, topic_id):
    """Добавляет новую запись по конкретной теме"""
    topic = Topic.objects.get(id=topic_id)

    popular_emojis = [
        '😀', '😂', '😍', '🥰', '😎', '🥳', '😭', '😡', '🤔',
        '👍', '👎', '👏', '🙌', '🙏', '💪', '🧠', '👀', '🎉', '💯',
        '📚', '📖', '✏️', '📝', '🔍', '💡', '✅', '❌', '📌', '🔗'
    ]

    if request.method != 'POST':
        # данные не отправлялись, создаётся пустая форма
        form = EntryForm()
    else:
        # Отправлены данные POST; обработать данные
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return redirect('learning_logs:topic', topic_id=topic_id)
    # вывести пустую или недействительную форму
    context = {
        'topic': topic,
        'form': form,
        'popular_emojis': popular_emojis,
    }
    return render(request, 'learning_logs/new_entry.html', context)


@login_required
def edit_entry(request, entry_id):
    """Редактирует существующую запись"""
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic

    popular_emojis = [
        '😀', '😂', '😍', '🥰', '😎', '🥳', '😭', '😡', '🤔',
        '👍', '👎', '👏', '🙌', '🙏', '💪', '🧠', '👀', '🎉', '💯',
        '📚', '📖', '✏️', '📝', '🔍', '💡', '✅', '❌', '📌', '🔗'
    ]

    if topic.owner != request.user:
        raise Http404

    if request.method != 'POST':
        # исходный запрос; форма заполняется данными текущей записи
        form = EntryForm(instance=entry)
    else:
        # отправка данных POST; обработать данные
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('learning_logs:topic', topic_id=topic.id)

    context = {
        'entry': entry,
        'topic': topic,
        'form': form,
        'popular_emojis': popular_emojis,
    }
    return render(request, 'learning_logs/edit_entry.html', context)


@login_required
def edit_topic(request, topic_id):
    """Редактирует существующую тему"""
    topic = get_object_or_404(Topic, id=topic_id)

    if topic.owner != request.user:
        raise Http404

    if request.method != 'POST':
        # исходный запрос; форма заполняется данными текущей записи
        form = TopicForm(instance=topic)
    else:
        # отправка данных POST; обработать данные
        form = TopicForm(instance=topic, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('learning_logs:topic', topic_id=topic.id)

    context = {'topic': topic, 'form': form}
    return render(request, 'learning_logs/edit_topic.html', context)

@login_required
def delete_topic(request, topic_id):
    """Удаляет тему и все связанные записи"""
    topic = get_object_or_404(Topic, id=topic_id)

    if topic.owner != request.user:
        raise Http404

    if request.method == 'POST':
        topic.delete()
        return redirect('learning_logs:topics')

    # Для подтверждения удаления можно показать страницу с вопросом
    context = {'topic': topic}
    return render(request, 'learning_logs/delete_topic.html', context)


@login_required
def delete_entry(request, entry_id):
    """Удаляет запись"""
    entry = get_object_or_404(Entry, id=entry_id)
    topic = entry.topic

    if topic.owner != request.user:
        raise Http404

    if request.method == 'POST':
        entry.delete()
        return redirect('learning_logs:topic', topic_id=topic.id)

    context = {'entry': entry, 'topic': topic}
    return render(request, 'learning_logs/delete_entry.html', context)


def export_topic(request, topic_id):
    """Экспортирует тему в JSON"""
    topic = get_object_or_404(Topic, id=topic_id, owner=request.user)
    entries = Entry.objects.filter(topic=topic).order_by('date_added')

    data = {
        "topic_name": topic.text,
        "entries": [
            {
                "text": entry.text,
                "date_added": entry.date_added.isoformat()
            }
            for entry in entries
        ]
    }

    filename = f"{slugify(topic.text)}_topic.json"
    response = HttpResponse(
        json.dumps(data, ensure_ascii=False, indent=2),
        content_type='application/json'
    )
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response


@login_required
def toggle_bookmark(request):
    """Переключает закладку для объекта (topic или entry)"""
    if request.method == 'POST':
        object_type = request.POST.get('type')  # 'topic' или 'entry'
        object_id = request.POST.get('id')

        if object_type == 'topic':
            obj = get_object_or_404(Topic, id=object_id, owner=request.user)
        elif object_type == 'entry':
            obj = get_object_or_404(Entry, id=object_id, topic__owner=request.user)
        else:
            return JsonResponse({'error': 'Invalid type'}, status=400)

        content_type = ContentType.objects.get_for_model(obj)
        bookmark, created = Bookmark.objects.get_or_create(
            user=request.user,
            content_type=content_type,
            object_id=obj.id
        )

        if not created:
            bookmark.delete()
            is_bookmarked = False
        else:
            is_bookmarked = True

        return JsonResponse({'is_bookmarked': is_bookmarked})
    return JsonResponse({'error': 'Invalid request'}, status=400)


@login_required
def bookmarks(request):
    bookmarks = Bookmark.objects.filter(user=request.user).select_related('content_type')

    topics = []
    entries = []

    for bm in bookmarks:
        if bm.content_type.model == 'topic':
            topic = bm.content_object
            if topic and topic.owner == request.user:
                topics.append(topic)
        elif bm.content_type.model == 'entry':
            entry = bm.content_object
            if entry and entry.topic.owner == request.user:
                entries.append(entry)

    return render(request, 'learning_logs/bookmarks.html', {
        'topics': topics,
        'entries': entries
    })
