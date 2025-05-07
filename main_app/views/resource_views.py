#main_app>views>resource_views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from ..models import SavedRecipe


# ──────────────── RESOURCE VIEWS ────────────────

@login_required
def resource_index(request):
    return render(request, 'resources/resource_index.html')

@login_required
def find_therapist(request):
    return render(request, 'resources/find_therapist.html')


# ──────────────── HEADSPACE VIEWS ────────────────

@login_required
def headspace_index(request):
    return render(request, 'resources/headspace_index.html')

@login_required
def headspace_meditations(request):
    videos = [
        {'title': 'Morning Energy Boost','video_id': 'FJG14EysFIA','url': 'https://www.youtube.com/watch?v=FJG14EysFIA'},
        {'title': '15-Minute Deep Relaxation Meditation','video_id': '2DXqMBXmP8Q','url': 'https://www.youtube.com/watch?v=2DXqMBXmP8Q'},
        {"title": "5 Minute Meditation", "video_id": "inpok4MKVLM"},
        {"title": "Body Scan for Beginners", "video_id": "ZToicYcHIOU"},
        {"title": "Calming Anxiety", "video_id": "MIr3RsUWrdo"},
        {"title": "Peaceful Piano + Rain", "video_id": "lFcSrYw-ARY"},
        {"title": "Deep Sleep Meditation", "video_id": "1ZYbU82GVz4"},
        {"title": "Lo-Fi Chill for Grounding", "video_id": "hHW1oY26kxQ"},
        {"title": "Breathwork for Clarity", "video_id": "kgTL5G1ibIo"},
        {"title": "Loving-Kindness Meditation", "video_id": "sz7cpV7ERsM"},
        {"title": "Gratitude Practice", "video_id": "O-6f5wQXSu8"},
        {"title": "Compassion Meditation", "video_id": "qzR62JJCMBQ"},
    ]
    return render(request, 'resources/headspace_meditations.html', {'videos': videos})

@login_required
def headspace_recipes(request):
    sections = ['Breakfast', 'Lunch', 'Dinner', 'Snacks', 'Teas / Drinks']
    recipes = [
        # ───────────── Breakfast ─────────────
        {
            'title': 'Creamy Blueberry-Pecan Oatmeal',
            'image': 'images/oats_berries.webp',
            'link': 'https://www.eatingwell.com/recipe/251104/creamy-blueberry-pecan-oatmeal/',
            'section': 'Breakfast'
        },
        {
            'title': 'Avocado Toast with Microgreens',
            'image': 'images/avocado_toast.jpg',
            'link': 'https://nourishedbynutrition.com/green-goddess-avocado-toast/?utm_source=chatgpt.com',
            'section': 'Breakfast'
        },
        {
            'title': 'Banana Nut Chia Pudding',
            'image': 'images/chia_pudding.jpg',
            'link': 'https://plantbasedrdblog.com/2024/02/banana-nut-chia-pudding/',
            'section': 'Breakfast'
        },

        # ───────────── Lunch ─────────────
        {
            'title': 'Lentil & Quinoa Nourish Bowl',
            'image': 'images/lentil_bowl.jpg',
            'link': 'https://cookingforpeanuts.com/high-protein-roasted-lentils-quinoa-bowl/?utm_source=chatgpt.com',
            'section': 'Lunch'
        },
        {
            'title': 'Mediterranean Chickpea Wraps',
            'image': 'images/chickpea_wraps.webp',
            'link': 'https://essycooks.com/easy-vegan-mediterranean-chickpea-wrap/?utm_source=chatgpt.com',
            'section': 'Lunch'
        },
        {
            'title': 'Rainbow Veggie Stir Fry',
            'image': 'images/veggie_stirfry.jpg',
            'link': 'https://www.joyoushealth.com/27520-blog-rainbow-veggie-stir-fry?utm_source=chatgpt.com',
            'section': 'Lunch'
        },

        # ───────────── Dinner ─────────────
        {
            'title': 'Butternut Squash Coconut Curry',
            'image': 'images/squash_curry.jpg',
            'link': 'https://naturallieplantbased.com/butternut-squash-curry/?utm_source=chatgpt.com',
            'section': 'Dinner'
        },
        {
            'title': 'Cauliflower Rice & Black Bean Tacos',
            'image': 'images/tacos.jpg',
            'link': 'https://nourishednutritioncounseling.com/cauliflower-and-black-bean-tacos/?utm_source=chatgpt.com',
            'section': 'Dinner'
        },
        {
            'title': 'Baked Salmon with Dill & Lemon',
            'image': 'images/salmon_dill.webp',
            'link': 'https://medium.com/simply-fresh/baked-salmon-with-lemon-and-dill-3b383e22f44a?utm_source=chatgpt.com',
            'section': 'Dinner'
        },

        # ───────────── Snacks ─────────────
        {
            'title': 'Energy Bites',
            'image': 'images/energy_bites.jpg',
            'link': 'https://fitfoodiefinds.com/peanut-butter-protein-balls-recipe/',
            'section': 'Snacks'
        },
        {
            'title': 'Roasted Chickpeas',
            'image': 'images/roasted-chickpeas.jpg',
            'link': 'https://www.loveandlemons.com/roasted-chickpeas/',
            'section': 'Snacks'
        },
        {
            'title': 'Apple Slices with Almond Butter',
            'image': 'images/apple_hemp.webp',
            'link': 'https://www.eatingwell.com/recipe/251354/apple-with-cinnamon-almond-butter/',
            'section': 'Snacks'
        },

        # ───────────── Teas / Drinks ─────────────
        {
            'title': 'Golden Turmeric Milk',
            'image': 'images/golden_milk.webp',
            'link': 'https://downshiftology.com/recipes/turmeric-milk-dairy-free/',
            'section': 'Teas / Drinks'
        },
        {
            'title': 'Chamomile Lavender Tea',
            'image': 'images/honey_chamomile_tea.webp',
            'link': 'https://www.thekitchn.com/honey-chamomile-tea-latte-264565',
            'section': 'Teas / Drinks'
        },
        {
            'title': 'Warm Lemon & Ginger Elixir',
            'image': 'images/lemon_ginger.webp',
            'link': 'https://www.allrecipes.com/recipe/256236/warm-lemon-honey-and-ginger-soother/',
            'section': 'Teas / Drinks'
        }
    ]

    return render(request, 'resources/headspace_recipes.html', {
        'recipes': recipes,
        'sections': sections  
    })


from django.shortcuts import redirect

@login_required
def save_recipe(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        image = request.POST.get('image')
        link = request.POST.get('link')
        user = request.user

        SavedRecipe.objects.get_or_create(
            user=user,
            title=title,
            image=image,
            link=link
        )
    messages.success(request, "Recipe saved to your profile!")
    return redirect('headspace-recipes')  

@login_required
def delete_saved_recipe(request, recipe_id):
    recipe = SavedRecipe.objects.get(id=recipe_id, user=request.user)
    recipe.delete()
    return redirect('profile')

from django.shortcuts import render

def gentle_workouts(request):
    return render(request, 'resources/gentle_workouts.html')

def decluttering_fengshui(request):
    return render(request, 'resources/decluttering_fengshui.html')

def mindfulness_retreats(request):
    return render(request, 'resources/mindfulness_retreats.html')

def vision_boards(request):
    return render(request, 'resources/vision_boards.html')



