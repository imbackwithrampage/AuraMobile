package com.aura.app.features.downloads

internal expect object DownloadsClock {
    fun nowEpochMs(): Long
}
