#pragma once

#include <stdbool.h>

typedef void (*AuraAppIconCompletion)(bool);

bool AuraSupportsAlternateAppIcons(void);
bool AuraIsCurrentAlternateAppIcon(const char *name);
void AuraSetAlternateAppIconName(const char *name, AuraAppIconCompletion completion);
