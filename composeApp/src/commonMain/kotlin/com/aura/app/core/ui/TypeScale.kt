package com.aura.app.core.ui

import androidx.compose.material3.MaterialTheme
import androidx.compose.runtime.Composable
import androidx.compose.runtime.staticCompositionLocalOf
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.text.font.FontWeight

data class NuvioTypeScale(
    val labelXs: TextStyle,
    val labelSm: TextStyle,
    val bodySm: TextStyle,
    val bodyMd: TextStyle,
    val bodyLg: TextStyle,
    val titleSm: TextStyle,
    val titleMd: TextStyle,
    val titleLg: TextStyle,
    val displaySm: TextStyle,
    val displayMd: TextStyle,
)

internal val LocalAuraTypeScale = staticCompositionLocalOf {
    NuvioTypeScale(
        labelXs = TextStyle(fontSize = AuraTokens.Type.labelXs, lineHeight = AuraTokens.LineHeight.labelXs, fontWeight = FontWeight.Medium),
        labelSm = TextStyle(fontSize = AuraTokens.Type.labelSm, lineHeight = AuraTokens.LineHeight.labelSm, fontWeight = FontWeight.Medium),
        bodySm = TextStyle(fontSize = AuraTokens.Type.bodySm, lineHeight = AuraTokens.LineHeight.bodySm, fontWeight = FontWeight.Normal),
        bodyMd = TextStyle(fontSize = AuraTokens.Type.bodyMd, lineHeight = AuraTokens.LineHeight.bodyMd, fontWeight = FontWeight.Normal),
        bodyLg = TextStyle(fontSize = AuraTokens.Type.bodyLg, lineHeight = AuraTokens.LineHeight.bodyLg, fontWeight = FontWeight.Medium),
        titleSm = TextStyle(fontSize = AuraTokens.Type.titleSm, lineHeight = AuraTokens.LineHeight.titleSm, fontWeight = FontWeight.Bold),
        titleMd = TextStyle(fontSize = AuraTokens.Type.titleMd, lineHeight = AuraTokens.LineHeight.titleMd, fontWeight = FontWeight.Bold),
        titleLg = TextStyle(fontSize = AuraTokens.Type.titleLg, lineHeight = AuraTokens.LineHeight.titleLg, fontWeight = FontWeight.Bold),
        displaySm = TextStyle(fontSize = AuraTokens.Type.displaySm, lineHeight = AuraTokens.LineHeight.displaySm, fontWeight = FontWeight.ExtraBold),
        displayMd = TextStyle(fontSize = AuraTokens.Type.displayMd, lineHeight = AuraTokens.LineHeight.displayMd, fontWeight = FontWeight.ExtraBold),
    )
}

val MaterialTheme.nuvioTypeScale: NuvioTypeScale
    @Composable
    get() = LocalAuraTypeScale.current
