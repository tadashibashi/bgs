from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from ..models import Game, Review


@login_required
def add_review(request, game_id):
    if request.method == 'POST':
        content = request.POST.get('content')
        rating = int(request.POST.get('rating'))
        game = get_object_or_404(Game, id=game_id)

        review = Review(
            content=content,
            rating=rating,
            user=request.user,
            game=game
        )
        review.save()
        return redirect('games_detail', pk=game_id)

@login_required
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)

    if review.user == request.user:
        game_id = review.game.id
        review.delete()

    return redirect('games_detail', pk=game_id)