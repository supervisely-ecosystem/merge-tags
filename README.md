<div align="center" markdown> 

# Merge Tags
  
<p align="center">

  <a href="#Overview">Overview</a> •
  <a href="#How-To-Run">How To Run</a> •
  <a href="#Notes">Notes</a>
</p>

</div>

## Overview 

Sometimes tags management can be tricky and time-consuming. This App helps to merge tags with the same value type. Let's consider several cases:

1. **Map one or several tags to the existing one**: all tags will be converted to destination tag meta and the source tags will be removed from project. Follow steps from (<a href="#How-To-Run">How To Run</a> section) 
2. **Map one or several tags to a new one**: first, you have to create new tag meta (on `Project`->`Tags` page) and then follow steps from (<a href="#How-To-Run">How To Run</a> section).

Notes:
- Result project name = original name + "(merged tags)" suffix
- Your data is safe: app creates new project with modified tags. The original project remains unchanged


## How To Run

### Step 1: Run from context menu of project

Go to "Context Menu" (images project or videos project) -> "Run App" -> "Transform" -> "Merge Tags"

### Step 2:  Waiting until the app is started
Once app is started, new task appear in workspace tasks. Wait message `Application is started ...` (1) and then press `Open` button (2).

### Step 3: Define mapping

App contains 3 sections: information about input project, information about output and the list of all tag metas from input project. In column `merge with` there are dropdown lists in front of each tag meta (row of the table). You have to define transformations for tags of interest. 

You can select several tag metas to merge with. Default option is no selection and means that tags will be copied without modification to a new project unless they are selected to merge with other tag. Dropdown lists only contain tag metas with same value type.

![merge-tags-screenshot](https://user-images.githubusercontent.com/61844772/230072269-f631331c-5f2f-4953-bede-fb7205ed6d08.png)

### Step 4: Press RUN button and wait

Press `Run` button. The progress bas will appear in `Output` section. Also you can monitor progress from tasks list of the current workspace.

App creates new project and it will appear in `Output` section. Result project name = original name + "(merged tags)" suffix

### Step 5: App shuts down automatically

Even if app is finished, you can always use it as a history: open it from tasks list in `Read Only` mode to view all information about a task: Input project, mapping settings and Output project. 
