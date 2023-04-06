<div align="center" markdown> 
<img src="https://user-images.githubusercontent.com/119248312/230250816-f63ac10f-26b6-4ea0-b0a4-21c5f58a7156.jpg" />

# Merge Tags
  
<p align="center">

  <a href="#Overview">Overview</a> •
  <a href="#How-To-Run">How To Run</a> •
  <a href="#Example-Screenshots">Example Screenshots</a>
</p>

[![](https://img.shields.io/badge/supervisely-ecosystem-brightgreen)](https://ecosystem.supervise.ly/apps/supervisely-ecosystem/merge-tags)
[![](https://img.shields.io/badge/slack-chat-green.svg?logo=slack)](https://supervise.ly/slack)
![GitHub release (latest SemVer)](https://img.shields.io/github/v/release/supervisely-ecosystem/merge-tags)
[![views](https://app.supervise.ly/img/badges/views/supervisely-ecosystem/merge-tags)](https://supervise.ly)
[![runs](https://app.supervise.ly/img/badges/runs/supervisely-ecosystem/merge-tags)](https://supervise.ly)

</div>

## Overview 

Sometimes tags management can be tricky and time-consuming. This App helps to merge tags with the same value type. Let's consider several cases:

1. **Map one or several tags to the existing one**: all tags will be converted to destination tag meta and the source tags will be removed from project. Follow steps from (<a href="#How-To-Run">How To Run</a> section) 
2. **Map one or several tags to a new one**: first, you have to create new tag meta (on `Project`->`Tags` page) and then follow steps from (<a href="#How-To-Run">How To Run</a> section).

Keep in mind that this project does not affect the original project or its meta, and only creates a new one with the modified tags.

## How To Run

1. Run the application from the context menu of a project

2. Wait until the app is started
Once app is started, new task appear in workspace tasks. Wait for the message `Application is started ...` and then press `Open` button.

3. Define mapping

App contains 3 sections: information about input project, information about output and the list of all tag metas from input project. In column `merge with` there are dropdown lists in front of each tag meta (row of the table). You have to define transformations for tags of interest. 

You can select several tag metas to merge with. Default option is no selection and means that tags will be copied without modification to a new project unless they are selected to merge with other tag. Dropdown lists only contain tag metas with same value type.

<img src="https://user-images.githubusercontent.com/119248312/230250580-70ccf1dc-6ea0-47d2-818a-a5cb41729e49.jpg" />

4. Press `RUN` button and wait

The progress bar will appear in `Output` section. Also you can monitor progress from tasks list of the current workspace.

App creates new project that will appear in `Output` section. Result project name is the original name with the "(merged tags)" suffix at the end.

5. No need to stop the app manually: it shuts down automatically

Even if app is finished, you can always use it as a history: open it from tasks list in `Read Only` mode to view all information about a task: Input project, mapping settings and Output project. 

## Example Screenshots

### Map one or several tags to the existing one
<div align="center" markdown> 

### Before
  
<img src="https://user-images.githubusercontent.com/119248312/230250570-1c7d01ba-37d3-4005-8dca-1e4d054d6a9f.jpg" />

### After
  
<img src="https://user-images.githubusercontent.com/119248312/230250572-5017114f-a354-4ed6-a172-1d6754dfdfef.jpg" />

</div>

### Map one or several tags to a new one
<div align="center" markdown> 

### Before

<img src="https://user-images.githubusercontent.com/119248312/230250565-ad68de7b-c9dd-4a05-a347-6d8d56deb77c.jpg" />

### After

<img src="https://user-images.githubusercontent.com/119248312/230250574-67c85992-3110-48f6-a3f7-bb2ff51c81ba.jpg" />

</div>
