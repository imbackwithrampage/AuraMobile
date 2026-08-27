package com.aura.app.features.library

internal expect object LibraryClock {
    fun nowEpochMs(): Long
}
