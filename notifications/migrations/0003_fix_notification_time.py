from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ("notifications", "0002_alter_notifications_notification_text"),
    ]

    operations = [
        migrations.RunSQL(
            """
            -- Add a temporary column with the correct type
            ALTER TABLE notifications_notifications
            ADD COLUMN notification_time_tz timestamptz;

            -- Fill the new column combining a fixed date with the existing time
            UPDATE notifications_notifications
            SET notification_time_tz = make_timestamptz(
                2025, 1, 1,
                extract(hour from notification_time)::int,
                extract(minute from notification_time)::int,
                extract(second from notification_time)::double precision,
                'UTC'
            );

            -- Drop the old column
            ALTER TABLE notifications_notifications
            DROP COLUMN notification_time;

            -- Rename the new column
            ALTER TABLE notifications_notifications
            RENAME COLUMN notification_time_tz TO notification_time;
            """
        ),
    ]
