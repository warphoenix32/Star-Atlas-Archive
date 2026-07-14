# Star Atlas Build

## Metadata

- Source ID: `SRC-OFF-D6F7E5EE3520E6EE`
- URL: https://build.staratlas.com/dev-resources/unreal-engine-tooling/how-to-setup-f-kit-in-your-project
- Publication date: UNKNOWN
- Updated date: 2026-04-16T16:32:35.000Z
- Original date text: 2026-04-16T16:32:35.000Z
- Author: ATMTA / Star Atlas official publisher
- Publisher: Star Atlas Build / ATMTA
- Document classification: `TECHNICAL_DOCUMENTATION`
- Extraction confidence: `MEDIUM`

## Official Authority Boundary

This record establishes what the named official publisher publicly stated and when. It does not by itself prove execution, independent economic accuracy, historical completeness, or absence of contrary evidence.

## Archival Abstract

Official technical documentation titled “Star Atlas Build.” This record preserves what Star Atlas Build / ATMTA publicly stated at the recorded publication time; claims about delivery, economics, or outcomes remain limited to the wording of the source.

## Products

- ATLAS
- F-KIT

## Actors and Organizations

- None identified.

## Governance

- None identified.

## Lore

- None identified.

## Classified Claims

- In our case the module we want to use is Foundation Open the .uproject file Add the plugin name you want to use for your project Close your IDE and generate project files again.
- Right-click .uproject file on the root directory and select Generate Visual Studio project files Open your project solution .sln You can now start using your plugin in C++

## Official Cross-References

- https://build.staratlas.com/dev-resources/unreal-engine-tooling/how-to-setup-f-kit-in-your-project
- https://build.staratlas.com/

## Temporal Validity

- Status: `CURRENT_DOCUMENTATION`
- Current validity: `CURRENT_PAGE_NOT_HISTORICAL_PROOF`
- Warning: Official publication does not independently prove successful execution, completeness, or continued current validity.

## Open Questions

- Which claims are independently corroborated or later superseded?

## Preserved Official Text

How To Setup F-Kit in Your Project | Star Atlas Build
Skip to contentStar Atlas BuildSearchK
Appearance
MenuReturn to top
How To Setup F-Kit in Your Project ​
Open Epic Games Launcher and launch your installed version of Unreal Engine
Create a new project and select C++ as project template
Close the editor and open the folder where the Project is located (e.g.,
C:\UnrealEngine\SampleProject
Create a new
Plugins
folder at the root directory
Copy your plugin within the
Plugins
directory
Right-click
.uproject
file located at the root and select
Generate Visual Studio project files
Double-click
.sln
file and open the project solution with your C++ IDE (Rider or Visual Studio)
Open the file located under
Source/<ProjectName>/<ProjectName>.build.cs
Addj to
PublicDependencyModuleNames
the plugin module name you want to use in C++. In our case the module we want to use is
Foundation
Open the
.uproject
file
Add the plugin name you want to use for your project
Close your IDE and generate project files again. Right-click
.uproject
file on the root directory and
select Generate Visual Studio project files
Open your project solution
.sln
You can now start using your plugin in C++
