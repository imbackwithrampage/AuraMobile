package com.aura.app

import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.remember
import androidx.compose.ui.Modifier
import com.aura.app.features.catalog.CatalogScreen
import com.aura.app.features.catalog.CatalogTarget
import com.aura.app.features.home.MetaPreview
import com.aura.app.features.library.toLibraryItem
import com.aura.app.navigation.CatalogRoute
import com.aura.app.navigation.DetailRoute
import com.aura.app.navigation.AuraNavigator

internal data class CatalogLaunch(
    val title: String,
    val subtitle: String,
    val target: CatalogTarget,
)

internal object CatalogLaunchStore {
    private var nextLaunchId = 1L
    private val launches = mutableMapOf<Long, CatalogLaunch>()

    fun put(launch: CatalogLaunch): Long {
        val launchId = nextLaunchId++
        launches[launchId] = launch
        return launchId
    }

    fun get(launchId: Long): CatalogLaunch? = launches[launchId]

    fun remove(launchId: Long) {
        launches.remove(launchId)
    }
}

@Composable
internal fun CatalogDestination(
    route: CatalogRoute,
    navController: AuraNavigator,
    onPosterLongClick: (PosterActionTarget) -> Unit,
) {
    val onBack = rememberGuardedPopBackStack(navController, route)
    val launch = remember(route.launchId) { CatalogLaunchStore.get(route.launchId) }
    if (launch == null) {
        LaunchedEffect(route.launchId) { onBack() }
        return
    }

    val target = launch.target
    CatalogScreen(
        title = launch.title,
        subtitle = launch.subtitle,
        target = target,
        onBack = onBack,
        onPosterClick = { meta ->
            navController.navigate(DetailRoute(type = meta.type, id = meta.id, title = meta.name))
        },
        onPosterLongClick = { meta: MetaPreview ->
            onPosterLongClick(
                if (target is CatalogTarget.Library) {
                    PosterActionTarget(
                        preview = meta,
                        libraryItem = meta.toLibraryItem(savedAtEpochMs = 0L),
                        libraryListKey = target.sectionType,
                    )
                } else {
                    PosterActionTarget(preview = meta)
                },
            )
        },
        modifier = Modifier.fillMaxSize(),
    )
}
