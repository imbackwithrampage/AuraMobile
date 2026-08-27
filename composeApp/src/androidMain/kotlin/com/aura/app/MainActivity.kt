package com.aura.app

import android.content.Intent
import android.content.res.Configuration
import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.activity.SystemBarStyle
import androidx.appcompat.app.AppCompatActivity
import androidx.core.splashscreen.SplashScreen.Companion.installSplashScreen
import com.aura.app.core.auth.AuthStorage
import com.aura.app.core.network.ServerConfigurationStorage
import com.aura.app.core.diagnostics.SentryInitializer
import com.aura.app.core.deeplink.handleAppUrl
import com.aura.app.core.storage.PlatformLocalAccountDataCleaner
import com.aura.app.core.sync.SyncClientIdentityStorage
import com.aura.app.features.addons.AddonHttpClientProvider
import com.aura.app.features.addons.AddonStorage
import com.aura.app.features.collection.CollectionMobileSettingsStorage
import com.aura.app.features.collection.CollectionStorage
import com.aura.app.features.debrid.DebridSettingsStorage
import com.aura.app.features.downloads.DownloadsLiveStatusPlatform
import com.aura.app.features.downloads.DownloadsPlatformDownloader
import com.aura.app.features.downloads.DownloadsStorage
import com.aura.app.features.library.LibraryDisplaySettingsStorage
import com.aura.app.features.membership.MemberAssetStorage
import com.aura.app.features.library.LibraryStorage
import com.aura.app.features.details.MetaScreenSettingsStorage
import com.aura.app.features.home.HomeCatalogSettingsStorage
import com.aura.app.features.mdblist.MdbListSettingsStorage
import com.aura.app.features.notifications.EpisodeReleaseNotificationPlatform
import com.aura.app.features.notifications.EpisodeReleaseNotificationsStorage
import com.aura.app.features.player.PlayerSettingsStorage
import com.aura.app.features.player.PlayerTrackPreferenceStorage
import com.aura.app.features.player.ExternalPlayerPlatform
import com.aura.app.features.player.SubtitleFileCache
import com.aura.app.features.player.PlayerPictureInPictureManager
import com.aura.app.features.player.PipRemoteActionReceiver
import com.aura.app.features.p2p.P2pSettingsStorage
import com.aura.app.features.p2p.P2pStreamingEngine
import com.aura.app.features.plugins.PluginStorage
import com.aura.app.features.profiles.AvatarStorage
import com.aura.app.features.profiles.ProfilePinCacheStorage
import com.aura.app.features.profiles.ProfileStorage
import com.aura.app.features.details.SeasonViewModeStorage
import com.aura.app.features.search.DiscoverSelectionStorage
import com.aura.app.features.search.SearchHistoryStorage
import com.aura.app.features.settings.SentrySettingsStorage
import com.aura.app.features.settings.AppIconPlatform
import com.aura.app.features.settings.ThemeSettingsStorage
import com.aura.app.features.trakt.TraktAuthStorage
import com.aura.app.features.trakt.TraktCommentsStorage
import com.aura.app.features.trakt.TraktLibraryStorage
import com.aura.app.features.trakt.TraktSettingsStorage
import com.aura.app.features.simkl.SimklAuthStorage
import com.aura.app.features.simkl.SimklSyncStorage
import com.aura.app.features.tmdb.TmdbSettingsStorage
import com.aura.app.features.updater.AndroidAppUpdaterPlatform
import com.aura.app.core.ui.CardDepthStyleStorage
import com.aura.app.core.ui.PosterCardStyleStorage
import com.aura.app.features.watched.WatchedStorage
import com.aura.app.features.streams.StreamLinkCacheStorage
import com.aura.app.features.streams.StreamBadgeSettingsStorage
import com.aura.app.features.streams.BingeGroupCacheStorage
import com.aura.app.features.watchprogress.ContinueWatchingEnrichmentStorage
import com.aura.app.features.watchprogress.ContinueWatchingPreferencesStorage
import com.aura.app.features.watchprogress.ResumePromptStorage
import com.aura.app.features.watchprogress.WatchProgressStorage

open class MainActivity : AppCompatActivity() {
    private var pipRemoteActionReceiver: PipRemoteActionReceiver? = null

    override fun onCreate(savedInstanceState: Bundle?) {
        installSplashScreen()
        enableEdgeToEdge(
            navigationBarStyle = SystemBarStyle.dark(
                scrim = 0xFF020404.toInt(),
            ),
        )
        ThemeSettingsStorage.initialize(applicationContext)
        AppIconPlatform.initialize(applicationContext)
        SentrySettingsStorage.initialize(applicationContext)
        SentryInitializer.start(application)
        super.onCreate(savedInstanceState)
        window.setBackgroundDrawableResource(R.color.aura_background)
        pipRemoteActionReceiver = PipRemoteActionReceiver.register(this)
        SyncClientIdentityStorage.initialize(applicationContext)
        AddonHttpClientProvider.initialize(applicationContext)
        AddonStorage.initialize(applicationContext)
        AuthStorage.initialize(applicationContext)
        ServerConfigurationStorage.initialize(applicationContext)
        LibraryStorage.initialize(applicationContext)
        WatchedStorage.initialize(applicationContext)
        MetaScreenSettingsStorage.initialize(applicationContext)
        HomeCatalogSettingsStorage.initialize(applicationContext)
        PlayerSettingsStorage.initialize(applicationContext)
        PlayerTrackPreferenceStorage.initialize(applicationContext)
        P2pSettingsStorage.initialize(applicationContext)
        P2pStreamingEngine.initialize(applicationContext)
        ExternalPlayerPlatform.initialize(applicationContext)
        SubtitleFileCache.initialize(applicationContext)
        ProfileStorage.initialize(applicationContext)
        AvatarStorage.initialize(applicationContext)
        ProfilePinCacheStorage.initialize(applicationContext)
        MemberAssetStorage.initialize(applicationContext)
        DiscoverSelectionStorage.initialize(applicationContext)
        SearchHistoryStorage.initialize(applicationContext)
        SeasonViewModeStorage.initialize(applicationContext)
        PosterCardStyleStorage.initialize(applicationContext)
        CardDepthStyleStorage.initialize(applicationContext)
        DebridSettingsStorage.initialize(applicationContext)
        TmdbSettingsStorage.initialize(applicationContext)
        MdbListSettingsStorage.initialize(applicationContext)
        TraktAuthStorage.initialize(applicationContext)
        TraktCommentsStorage.initialize(applicationContext)
        TraktLibraryStorage.initialize(applicationContext)
        TraktSettingsStorage.initialize(applicationContext)
        SimklAuthStorage.initialize(applicationContext)
        SimklSyncStorage.initialize(applicationContext)
        LibraryDisplaySettingsStorage.initialize(applicationContext)
        ContinueWatchingPreferencesStorage.initialize(applicationContext)
        ResumePromptStorage.initialize(applicationContext)
        ContinueWatchingEnrichmentStorage.initialize(applicationContext)
        EpisodeReleaseNotificationsStorage.initialize(applicationContext)
        WatchProgressStorage.initialize(applicationContext)
        StreamLinkCacheStorage.initialize(applicationContext)
        StreamBadgeSettingsStorage.initialize(applicationContext)
        BingeGroupCacheStorage.initialize(applicationContext)
        PluginStorage.initialize(applicationContext)
        CollectionMobileSettingsStorage.initialize(applicationContext)
        CollectionStorage.initialize(applicationContext)
        DownloadsStorage.initialize(applicationContext)
        DownloadsPlatformDownloader.initialize(applicationContext)
        DownloadsLiveStatusPlatform.initialize(applicationContext)
        AndroidAppUpdaterPlatform.initialize(applicationContext)
        PlatformLocalAccountDataCleaner.initialize(applicationContext)
        EpisodeReleaseNotificationPlatform.initialize(applicationContext)
        EpisodeReleaseNotificationPlatform.bindActivity(this)
        handleIncomingAppIntent(intent)

        setContent {
            App()
        }
    }

    override fun onNewIntent(intent: Intent) {
        super.onNewIntent(intent)
        setIntent(intent)
        handleIncomingAppIntent(intent)
    }

    override fun onUserLeaveHint() {
        super.onUserLeaveHint()
        PlayerPictureInPictureManager.onUserLeaveHint(this)
    }

    override fun onPictureInPictureModeChanged(
        isInPictureInPictureMode: Boolean,
        newConfig: Configuration,
    ) {
        super.onPictureInPictureModeChanged(isInPictureInPictureMode, newConfig)
        PlayerPictureInPictureManager.onPictureInPictureModeChanged(this, isInPictureInPictureMode)
    }

    override fun onDestroy() {
        EpisodeReleaseNotificationPlatform.unbindActivity(this)
        val receiver = pipRemoteActionReceiver
        if (receiver != null) {
            runCatching { unregisterReceiver(receiver) }
            pipRemoteActionReceiver = null
        }
        super.onDestroy()
    }

    override fun onRequestPermissionsResult(
        requestCode: Int,
        permissions: Array<String>,
        grantResults: IntArray,
    ) {
        if (EpisodeReleaseNotificationPlatform.handlePermissionRequestResult(requestCode, grantResults)) {
            return
        }
        super.onRequestPermissionsResult(requestCode, permissions, grantResults)
    }

    private fun handleIncomingAppIntent(intent: Intent?) {
        val appUrl = intent?.dataString?.trim().orEmpty()
        if (appUrl.isBlank()) return
        handleAppUrl(appUrl)
    }
}
