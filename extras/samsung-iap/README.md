# Samsung IAP (nicht aktiv)

`SamsungIapPlugin.java` wurde aus dem Android-Build genommen, weil die Samsung
IAP-SDK-Bibliothek (`IAP6Helper`) im Projekt fehlt und der Build damit nicht
kompiliert. Für den Google-Play-Build wird sie nicht gebraucht.

Zum Aktivieren später:
1. Samsung IAP SDK als Modul `:IAP6Helper` einbinden und in `android/app/build.gradle` aktivieren.
2. Datei zurück nach `android/app/src/main/java/com/enesdoudouzi/iqtest/samsungiap/` kopieren.
3. In `MainActivity.java` `registerPlugin(SamsungIapPlugin.class)` vor `super.onCreate(...)` ergänzen.
4. In `AndroidManifest.xml` `com.samsung.android.iap.permission.BILLING` ergänzen.
5. In `app.js` `STORE_TARGET = 'galaxy'` setzen und Samsung-Item-IDs eintragen.
