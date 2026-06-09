from .models import EmergencyNotification


FIELDS = ["title", "content", "level", "target_group", "is_active"]


def serialize_notification(notification):
    return {
        "id": notification.id,
        "title": notification.title,
        "content": notification.content,
        "level": notification.level,
        "target_group": notification.target_group,
        "is_active": notification.is_active,
        "published_at": notification.published_at.isoformat(),
        "updated_at": notification.updated_at.isoformat(),
    }


LEVEL_ORDER = {"critical": 0, "warning": 1, "info": 2}


def list_notifications(active=None, level=None, target_group=None):
    queryset = EmergencyNotification.objects.all()
    if active is not None:
        queryset = queryset.filter(is_active=active)
    if level:
        queryset = queryset.filter(level=level)
    if target_group:
        queryset = queryset.filter(target_group=target_group)
    results = [serialize_notification(item) for item in queryset]
    results.sort(key=lambda n: n["published_at"], reverse=True)
    results.sort(key=lambda n: LEVEL_ORDER.get(n["level"], 99))
    return results


def create_notification(payload):
    data = {field: payload.get(field) for field in FIELDS if field in payload}
    return EmergencyNotification(**data)


def update_notification(notification, payload):
    for field in FIELDS:
        if field in payload:
            setattr(notification, field, payload[field])
    notification.save()
    return notification
