# Copyright (C) Lutra Consulting Limited
#
# SPDX-License-Identifier: AGPL-3.0-only OR LicenseRef-MerginMaps-Commercial

import os
from flask import current_app, abort
from sqlalchemy import event

from ..app import db

from ..lang.current import returnTranslation

def check(session):
    if os.path.isfile(current_app.config["MAINTENANCE_FILE"]):
        ServiceUnavailableDueToMaintenancePleaseTryLater = returnTranslation("ServiceUnavailableDueToMaintenancePleaseTryLater")
        abort(503, ServiceUnavailableDueToMaintenancePleaseTryLater)


def register_events():
    event.listen(db.session, "before_commit", check)


def remove_events():
    event.remove(db.session, "before_commit", check)
