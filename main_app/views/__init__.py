# main_app>views>__init__.py
from .main_views import (
    home,
    about,
    signup,
    login_view,
    profile,
    edit_profile,
    delete_profile,
)

from .habit_views import (
    habit_index,
    habit_create,
    habit_detail,
    habit_edit,
    habit_delete,
    add_checkin,
    toggle_checkin,
)

from .reflection_views import (
    reflection_index, 
    reflection_create, 
    reflection_detail, 
    reflection_edit, 
    reflection_delete,
)

from .mood_views import (
    mood_index,
    mood_create,
    mood_detail,
    mood_edit,
    mood_delete,
)

from .resource_views import (
    resource_index,
    find_therapist,
    headspace_index,
    headspace_meditations,
)

from .onboarding_views import (
    onboarding_start, 
    select_habits, 
    onboarding_mood
)