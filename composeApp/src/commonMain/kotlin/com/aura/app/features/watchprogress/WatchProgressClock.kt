package com.aura.app.features.watchprogress

internal expect object WatchProgressClock {
    fun nowEpochMs(): Long
}
