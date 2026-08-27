package com.aura.app.core.ui

import androidx.compose.runtime.Composable
import androidx.compose.ui.graphics.painter.Painter
import aura.composeapp.generated.resources.Res
import aura.composeapp.generated.resources.ic_player_aspect_ratio
import aura.composeapp.generated.resources.ic_player_audio_filled
import aura.composeapp.generated.resources.ic_player_pause
import aura.composeapp.generated.resources.ic_player_play
import aura.composeapp.generated.resources.ic_player_subtitles
import aura.composeapp.generated.resources.library_add_plus
import org.jetbrains.compose.resources.painterResource

@Composable
actual fun appIconPainter(icon: AppIconResource): Painter =
    painterResource(
        when (icon) {
            AppIconResource.PlayerPlay -> Res.drawable.ic_player_play
            AppIconResource.PlayerPause -> Res.drawable.ic_player_pause
            AppIconResource.PlayerAspectRatio -> Res.drawable.ic_player_aspect_ratio
            AppIconResource.PlayerSubtitles -> Res.drawable.ic_player_subtitles
            AppIconResource.PlayerAudioFilled -> Res.drawable.ic_player_audio_filled
            AppIconResource.LibraryAddPlus -> Res.drawable.library_add_plus
        }
    )
