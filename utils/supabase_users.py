import requests
import os

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")

headers = {
    "apikey": SUPABASE_ANON_KEY,
    "Authorization": f"Bearer {SUPABASE_ANON_KEY}",
    "Content-Type": "application/json",
    "Prefer": "resolution=merge-duplicates"
}


def save_user(user):
    url = f"{SUPABASE_URL}/rest/v1/users"
    payload = {
        "telegram_id": str(user.id),
        "first_name": user.first_name,
        "username": user.username
    }
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code not in (200, 201):
        print("❌ Ошибка при сохранении пользователя:", response.text)
    else:
        print("✅ Пользователь сохранён/обновлён")


def increment_counter(user_id, field="parables_count"):
    assert field in ["parables_count", "wisdoms_count"], "❗ Неверное поле!"

    # Получаем текущую запись
    url = f"{SUPABASE_URL}/rest/v1/users?telegram_id=eq.{user_id}"
    get_resp = requests.get(url, headers=headers)

    if get_resp.status_code == 200 and get_resp.json():
        current = get_resp.json()[0].get(field, 0)
        new_value = current + 1

        # Обновляем значение
        update_payload = {field: new_value}
        patch_resp = requests.patch(url, json=update_payload, headers=headers)

        if patch_resp.status_code in (204, 200):
            print(f"✅ Поле {field} обновлено до {new_value}")
        else:
            print(f"❌ Ошибка при обновлении {field}:", patch_resp.text)
    else:
        print("❌ Пользователь не найден при обновлении счётчика.")
