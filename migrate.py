import json
from database import get_source_db, get_target_db
from email_alert import send_alert

CHECKPOINT_FILE = "checkpoint.json"


def load_checkpoint() -> int:
    try:
        with open(CHECKPOINT_FILE, "r") as f:
            return json.load(f)["last_id"]
    except (FileNotFoundError, KeyError, json.JSONDecodeError):
        return 0


def save_checkpoint(last_id: int) -> None:
    with open(CHECKPOINT_FILE, "w") as f:
        json.dump({"last_id": last_id}, f)


def migrate() -> None:
    source_db = get_source_db()
    target_db = get_target_db()

    source_cursor = source_db.cursor()
    target_cursor = target_db.cursor()

    last_id = load_checkpoint()
    print(f"Starting migration from ID > {last_id}")

    source_cursor.execute(
        "SELECT id, customer_name, amount FROM orders WHERE id > ? ORDER BY id",
        (last_id,)
    )

    rows = source_cursor.fetchall()

    for order_id, customer_name, amount in rows:
        try:
            if amount < 0:
                raise ValueError(
                    f"Invalid amount detected for order ID {order_id}"
                )

            target_cursor.execute(
                "INSERT INTO orders (id, customer_name, amount) VALUES (?, ?, ?)",
                (order_id, customer_name, amount)
            )
            target_db.commit()

            save_checkpoint(order_id)
            print(f"Migrated order ID {order_id}")

        except Exception as error:
            save_checkpoint(order_id)
            send_alert(str(error))
            print(f"Migration stopped: {error}")
            break

    source_db.close()
    target_db.close()


if __name__ == "__main__":
    migrate()
