from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Sum, Count
from django.db import connection
from .models import SavingsBox
import json


def index(request):
    """Main view displaying the savings tracker grid"""
    boxes = SavingsBox.objects.all()
    
    # Initialize boxes if none exist
    if not boxes.exists():
        SavingsBox.initialize_boxes()
        boxes = SavingsBox.objects.all()
    
    # Calculate progress
    total_amount = boxes.aggregate(Sum('value'))['value__sum'] or 0
    saved_amount = boxes.filter(is_saved=True).aggregate(Sum('value'))['value__sum'] or 0
    progress_percentage = (saved_amount / total_amount * 100) if total_amount > 0 else 0
    
    context = {
        'boxes': boxes,
        'total_amount': total_amount,
        'saved_amount': saved_amount,
        'progress_percentage': round(progress_percentage, 1),
        'target_amount': 100000,
    }
    
    return render(request, 'tracker/index.html', context)


@csrf_exempt
@require_POST
def toggle_box(request, box_id):
    """Toggle the saved status of a savings box"""
    try:
        box = get_object_or_404(SavingsBox, id=box_id)
        box.is_saved = not box.is_saved
        box.save()
        
        # Calculate updated progress
        boxes = SavingsBox.objects.all()
        total_amount = boxes.aggregate(Sum('value'))['value__sum'] or 0
        saved_amount = boxes.filter(is_saved=True).aggregate(Sum('value'))['value__sum'] or 0
        progress_percentage = (saved_amount / total_amount * 100) if total_amount > 0 else 0
        
        return JsonResponse({
            'success': True,
            'is_saved': box.is_saved,
            'saved_amount': saved_amount,
            'total_amount': total_amount,
            'progress_percentage': round(progress_percentage, 1),
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})




def reset_progress(request):
    """Reset all saved progress"""
    if request.method == 'POST':
        SavingsBox.objects.all().update(is_saved=False)
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})


def logout_view(request):
    """Logout and clear authentication session"""
    request.session.pop('authenticated', None)
    return HttpResponse("<h1>Logged out successfully</h1><p><a href='/'>Return to login</a></p>")


def initialize_boxes_view(request):
    """Re-initialize all savings boxes"""
    if request.method == 'POST':
        SavingsBox.initialize_boxes()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})
