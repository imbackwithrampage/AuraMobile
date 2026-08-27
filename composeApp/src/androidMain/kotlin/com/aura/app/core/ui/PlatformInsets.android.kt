package com.aura.app.core.ui

import androidx.compose.foundation.layout.WindowInsets
import androidx.compose.foundation.layout.asPaddingValues
import androidx.compose.foundation.layout.navigationBars
import androidx.compose.foundation.layout.statusBars
import androidx.compose.runtime.Composable
import androidx.compose.ui.unit.Dp
import androidx.compose.ui.unit.dp

internal actual val auraPlatformExtraTopPadding: Dp = 0.dp
internal actual val auraPlatformExtraBottomPadding: Dp = 0.dp
internal actual val auraBottomNavigationExtraVerticalPadding: Dp = 6.dp
@Composable
internal actual fun auraBottomNavigationBarInsets(): WindowInsets = WindowInsets.navigationBars

@Composable
internal actual fun platformPhysicalTopInset(): Dp =
    WindowInsets.statusBars.asPaddingValues().calculateTopPadding()
