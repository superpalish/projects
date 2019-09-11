#!/bin/sh

if [ ! -f /plates/.migration-done ]; then
  /usr/bin/yes "yes" | python /plates/plates-project/manage.py migrate && /bin/touch /plates/.migration-done
fi

python /plates/plates-project/manage.py collectstatic --link --noinput

echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'plates')" | python /plates/plates-project/manage.py shell

exec "$@"
