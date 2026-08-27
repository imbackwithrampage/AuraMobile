package com.aura.app.core.storage

import com.aura.app.core.build.AppFeaturePolicy
import com.aura.app.core.sync.SyncManager
import com.aura.app.core.sync.ProfileSettingsSync
import com.aura.app.core.tracking.ensureTrackingProvidersRegistered
import com.aura.app.features.addons.AddonRepository
import com.aura.app.features.catalog.CatalogRepository
import com.aura.app.features.collection.CollectionMobileSettingsRepository
import com.aura.app.features.collection.CollectionRepository
import com.aura.app.features.details.MetaDetailsRepository
import com.aura.app.features.details.MetaScreenSettingsRepository
import com.aura.app.features.home.HomeCatalogSettingsRepository
import com.aura.app.features.home.HomeRepository
import com.aura.app.features.library.LibraryRepository
import com.aura.app.features.membership.MemberAccessRepository
import com.aura.app.features.library.LibraryDisplaySettingsRepository
import com.aura.app.features.notifications.EpisodeReleaseNotificationsRepository
import com.aura.app.features.player.PlayerLaunchStore
import com.aura.app.features.player.PlayerSettingsRepository
import com.aura.app.features.p2p.P2pSettingsRepository
import com.aura.app.features.plugins.PluginRepository
import com.aura.app.features.player.SubtitleRepository
import com.aura.app.features.profiles.ProfileRepository
import com.aura.app.features.profiles.MAX_PROFILES
import com.aura.app.features.search.SearchRepository
import com.aura.app.features.settings.ThemeSettingsRepository
import com.aura.app.features.streams.StreamContextStore
import com.aura.app.features.streams.StreamBadgeSettingsRepository
import com.aura.app.features.streams.StreamLaunchStore
import com.aura.app.features.streams.StreamsRepository
import com.aura.app.features.tracking.TrackingProviderRegistry
import com.aura.app.features.tracking.TrackingSettingsRepository
import com.aura.app.core.ui.CardDepthStyleRepository
import com.aura.app.core.ui.PosterCardStyleRepository
import com.aura.app.features.watchprogress.ContinueWatchingPreferencesRepository
import com.aura.app.features.watchprogress.ContinueWatchingEnrichmentCache
import com.aura.app.features.watchprogress.WatchProgressRepository
import com.aura.app.features.watchprogress.WatchProgressSourceCoordinator
import com.aura.app.features.watched.WatchedRepository

internal object LocalAccountDataCleaner {
    fun wipe() {
        ensureTrackingProvidersRegistered()
        TrackingProviderRegistry.removeStoredProfiles(1..MAX_PROFILES)
        SyncManager.cancelAccountSync()
        WatchProgressSourceCoordinator.clearLocalState()
        ProfileSettingsSync.clearAccountState()
        ContinueWatchingEnrichmentCache.clearLocalState()
        WatchProgressRepository.clearLocalState()
        WatchedRepository.clearLocalState()
        LibraryRepository.runAccountStorageWipe {
            PlatformLocalAccountDataCleaner.wipe()
        }

        ProfileRepository.clearInMemory()
        MemberAccessRepository.clearLocalState()
        AddonRepository.clearLocalState()
        if (AppFeaturePolicy.pluginsEnabled) {
            PluginRepository.clearLocalState()
        }
        HomeRepository.clear()
        HomeCatalogSettingsRepository.clearLocalState()
        MetaScreenSettingsRepository.clearLocalState()
        LibraryRepository.clearLocalState()
        LibraryDisplaySettingsRepository.clearLocalState()
        ContinueWatchingPreferencesRepository.clearLocalState()
        EpisodeReleaseNotificationsRepository.clearLocalState()
        CollectionMobileSettingsRepository.clearLocalState()
        CollectionRepository.clearLocalState()
        ThemeSettingsRepository.clearLocalState()
        PosterCardStyleRepository.clearLocalState()
        CardDepthStyleRepository.clearLocalState()
        TrackingProviderRegistry.clearLocalState()
        TrackingSettingsRepository.clearLocalState()
        PlayerSettingsRepository.clearLocalState()
        StreamBadgeSettingsRepository.clearLocalState()
        P2pSettingsRepository.clearLocalState()
        CatalogRepository.clear()
        StreamsRepository.clear()
        MetaDetailsRepository.clear()
        SearchRepository.reset()
        SubtitleRepository.clear()
        PlayerLaunchStore.clear()
        StreamLaunchStore.clear()
        StreamContextStore.clear()
    }
}

internal expect object PlatformLocalAccountDataCleaner {
    fun wipe()
}
