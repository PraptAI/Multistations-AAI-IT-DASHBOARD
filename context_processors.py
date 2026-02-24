def user_station_context(request):
    user_station_name = None
    if request.user.is_authenticated:
        profile = getattr(request.user, "userprofile", None)
        if profile and getattr(profile, "station", None):
            user_station_name = profile.station.name
    return {"user_station_name": user_station_name}