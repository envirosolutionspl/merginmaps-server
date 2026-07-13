// Copyright (C) Lutra Consulting Limited
//
// SPDX-License-Identifier: AGPL-3.0-only OR LicenseRef-MerginMaps-Commercial

import {
  DialogModule,
  FormModule,
  UserModule,
  NotificationModule,
  moduleUtils,
  getHttpService,
  ProjectModule,
  LayoutModule,
  InstanceModule,
  useInstanceStore,
  initCsrfToken
} from '@mergin/lib'

import 'primevue/resources/primevue.min.css'
import 'primeflex/primeflex.min.css'
import '@mergin/lib/dist/sass/themes/mm-theme-light/theme.scss'
import '@tabler/icons-webfont/tabler-icons.min.css'
import '@mergin/lib/dist/style.css'

import { createMerginApp } from './app'
import { createPiniaInstance, getPiniaInstance } from './store'

(function() {
  'use strict';

  let lastEventDate = null;

  // Funkcja logująca aktywność
  function logActivity() {
      const date = Math.floor(Date.now() / 1000);
      lastEventDate = date;
  }

  setInterval(async () => {
    if(window.location.pathname === '/login/reset' || window.location.pathname === '/login') {
      return
    }
    try {
      const csrf_req = await fetch('/app/auth/refresh/csrf', { credentials: "include" });
      const csrf_res = await csrf_req.json();
      const csrf = csrf_res.csrf;

      const response = await fetch('/app/auth/check_session', {
        method: 'POST',
        body: JSON.stringify({
          time: lastEventDate
        }),
        headers: {
          'Content-Type': 'application/json',
          'X-CSRF-Token': csrf
        },
        credentials: 'include'
      });

      const data = await response.json();
      if (!data.authenticated) {
        setTimeout(() => {
          window.location.href = '/login'
        }, 100);
      }
    } catch(e) {
      window.location.href = '/login';
    }
  }, 10000);

  // Śledzenie ruchu myszy
  document.addEventListener('mousemove', function(e) {
      logActivity();
  });

  // Śledzenie kliknięć myszy
  document.addEventListener('click', function(e) {
    logActivity();
  });

  // Śledzenie naciśnięć klawiszy
  document.addEventListener('keydown', function(e) {
    logActivity();
  });

  // Śledzenie przewijania strony
  document.addEventListener('scroll', function(e) {
    logActivity();
  });

  // Śledzenie dotknięć na urządzeniach mobilnych
  document.addEventListener('touchstart', function(e) {
    logActivity();
  });

  // Śledzenie zmiany rozmiaru okna
  window.addEventListener('resize', function(e) {
    logActivity();
  });

  // Śledzenie fokusowania elementów
  document.addEventListener('focusin', function(e) {
    logActivity();
  });

  // Śledzenie wpisywania w pola tekstowe
  document.addEventListener('input', function(e) {
    logActivity();
  });

})();

async function main() {
  createPiniaInstance()
  const pinia = getPiniaInstance()
  const httpService = getHttpService()

  // initialize modules
  moduleUtils.initializeAppModule(LayoutModule)
  moduleUtils.initializeAppModule(UserModule, {
    httpService
  })
  moduleUtils.initializeAppModule(NotificationModule)
  moduleUtils.initializeAppModule(DialogModule)
  moduleUtils.initializeAppModule(FormModule)
  moduleUtils.initializeAppModule(ProjectModule, {
    httpService
  })
  moduleUtils.initializeAppModule(InstanceModule, {
    httpService
  })

  // App initialization
  const instanceStore = useInstanceStore(pinia)
  const response = await instanceStore.initApp()
  initCsrfToken(response)
  createMerginApp().mount('#app')
  // checkToken()
}

main()
