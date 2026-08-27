package com.aura.app.core.tracking

import com.aura.app.features.simkl.SimklAuthRepository
import com.aura.app.features.simkl.SimklMutationRepository
import com.aura.app.features.simkl.SimklLibraryRepository
import com.aura.app.features.simkl.SimklProgressRepository
import com.aura.app.features.simkl.SimklTrackingLibraryProvider
import com.aura.app.features.simkl.SimklTrackingProgressProvider
import com.aura.app.features.simkl.SimklWatchedSyncAdapter
import com.aura.app.features.simkl.SimklSyncRepository
import com.aura.app.features.tracking.TrackingProviderRegistry
import com.aura.app.features.trakt.TraktAuthRepository
import com.aura.app.features.trakt.TraktScrobbleRepository
import com.aura.app.features.trakt.TraktTrackingLibraryProvider
import com.aura.app.features.trakt.TraktTrackingProgressProvider
import com.aura.app.features.watching.sync.TraktWatchedSyncAdapter

fun ensureTrackingProvidersRegistered() {
    TraktAuthRepository.descriptor
    TraktScrobbleRepository.ensureRegistered()
    SimklAuthRepository.descriptor
    SimklSyncRepository.state
    SimklLibraryRepository.uiState
    SimklProgressRepository.uiState
    SimklMutationRepository.ensureRegistered()
    TrackingProviderRegistry.registerLibraryProvider(TraktTrackingLibraryProvider)
    TrackingProviderRegistry.registerLibraryProvider(SimklTrackingLibraryProvider)
    TrackingProviderRegistry.registerWatchedProvider(TraktWatchedSyncAdapter)
    TrackingProviderRegistry.registerWatchedProvider(SimklWatchedSyncAdapter)
    TrackingProviderRegistry.registerProgressProvider(TraktTrackingProgressProvider)
    TrackingProviderRegistry.registerProgressProvider(SimklTrackingProgressProvider)
}
