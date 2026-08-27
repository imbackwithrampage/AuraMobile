package com.aura.app.features.settings

import aura.composeapp.generated.resources.Res
import aura.composeapp.generated.resources.lang_arabic
import aura.composeapp.generated.resources.lang_bulgarian
import aura.composeapp.generated.resources.lang_czech
import aura.composeapp.generated.resources.lang_english
import aura.composeapp.generated.resources.lang_french
import aura.composeapp.generated.resources.lang_german
import aura.composeapp.generated.resources.lang_greek
import aura.composeapp.generated.resources.lang_hebrew
import aura.composeapp.generated.resources.lang_hungarian
import aura.composeapp.generated.resources.lang_indonesian
import aura.composeapp.generated.resources.lang_italian
import aura.composeapp.generated.resources.lang_polish
import aura.composeapp.generated.resources.lang_portuguese_brazil
import aura.composeapp.generated.resources.lang_portuguese_portugal
import aura.composeapp.generated.resources.lang_romanian
import aura.composeapp.generated.resources.lang_slovak
import aura.composeapp.generated.resources.lang_spanish
import aura.composeapp.generated.resources.lang_turkish
import aura.composeapp.generated.resources.lang_norwegian
import aura.composeapp.generated.resources.lang_dutch
import aura.composeapp.generated.resources.lang_japanese
import aura.composeapp.generated.resources.lang_vietnamese
import aura.composeapp.generated.resources.settings_appearance_app_language_device
import org.jetbrains.compose.resources.StringResource

enum class AppLanguage(
    val code: String,
    val labelRes: StringResource,
) {
    DEVICE("device", Res.string.settings_appearance_app_language_device),
    ARABIC("ar", Res.string.lang_arabic),
    BULGARIAN("bg", Res.string.lang_bulgarian),
    CZECH("cs", Res.string.lang_czech),
    ENGLISH("en", Res.string.lang_english),
    FRENCH("fr", Res.string.lang_french),
    GERMAN("de", Res.string.lang_german),
    GREEK("el", Res.string.lang_greek),
    HEBREW("he", Res.string.lang_hebrew),
    HUNGARIAN("hu", Res.string.lang_hungarian),
    INDONESIAN("id", Res.string.lang_indonesian),
    ITALIAN("it", Res.string.lang_italian),
    POLISH("pl", Res.string.lang_polish),
    PORTUGUESE_BRAZIL("pt-BR", Res.string.lang_portuguese_brazil),
    PORTUGUESE("pt", Res.string.lang_portuguese_portugal),
    ROMANIAN("ro", Res.string.lang_romanian),
    SLOVAK("sk", Res.string.lang_slovak),
    SPANISH("es", Res.string.lang_spanish),
    TURKISH("tr", Res.string.lang_turkish),
    NORWEGIAN("nb", Res.string.lang_norwegian),
    DUTCH("nl", Res.string.lang_dutch),
    JAPANESE("ja", Res.string.lang_japanese),
    VIETNAMESE("vi", Res.string.lang_vietnamese),
    ;

    companion object {
        fun fromCode(code: String?): AppLanguage =
            entries.firstOrNull { it.code.equals(code, ignoreCase = true) } ?: DEVICE
    }
}
