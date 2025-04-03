<!-- src/components/ProjectsHistogram.vue -->
<template>
    <div class="histogram-container">
      <div class="header">
        <h2>Files Distribution Across Projects</h2>
        <div class="stats-summary">
          <div class="stat-item">
            <span class="stat-value">{{ totalProjects }}</span>
            <span class="stat-label">Projects</span>
          </div>
          <div class="stat-item">
            <span class="stat-value">{{ totalFiles }}</span>
            <span class="stat-label">Total Files</span>
          </div>
          <div class="stat-item">
            <span class="stat-value">{{ avgFilesPerProject.toFixed(1) }}</span>
            <span class="stat-label">Avg Files/Project</span>
          </div>
        </div>
      </div>
  
      <div class="histogram-wrapper">
        <div class="y-axis">
          <div v-for="(tick, index) in yAxisTicks" :key="index" class="y-tick">
            <span class="tick-value">{{ tick }}</span>
            <span class="tick-line"></span>
          </div>
        </div>
        
        <div class="histogram">
          <div 
            v-for="project in projectsWithFileCount" 
            :key="project._id" 
            class="bar-container"
            @click="onBarClick(project)"
          >
            <div class="bar-tooltip">
              {{ project.name }}: {{ project.fileCount }} files
              ({{ getPercentage(project.fileCount) }}%)
            </div>
            <div 
              class="bar" 
              :style="{ height: getBarHeight(project.fileCount) + 'px' }"
            ></div>
            <div class="value-label">{{ project.fileCount }}</div>
            <div class="label">{{ project.name }}</div>
          </div>
        </div>
      </div>
  
      <div class="legend">
        <div class="legend-item">
          <span class="legend-color" style="background-color: #292961;"></span>
          <span class="legend-text">Number of files</span>
        </div>
        <div v-if="selectedProject" class="selected-project">
          Selected: <strong>{{ selectedProject.name }}</strong> 
          ({{ selectedProject.fileCount }} files)
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    props: {
      projects: {
        type: Array,
        required: true
      },
      files: {
        type: Array,
        required: true
      }
    },
    data() {
      return {
        selectedProject: null,
        yAxisTicksCount: 5
      };
    },
    computed: {
      projectsWithFileCount() {
        return this.projects.map(project => {
          const fileCount = this.files.filter(file => 
            file.projectID && file.projectID.includes(project._id)
          ).length;
          return {
            ...project,
            fileCount
          };
        }).sort((a, b) => b.fileCount - a.fileCount); // Сортировка по убыванию
      },
      maxFileCount() {
        return Math.max(...this.projectsWithFileCount.map(p => p.fileCount), 1);
      },
      totalProjects() {
        return this.projects.length;
      },
      totalFiles() {
        return this.files.length;
      },
      avgFilesPerProject() {
        return this.totalFiles / this.totalProjects;
      },
      yAxisTicks() {
        const ticks = [];
        const step = Math.ceil(this.maxFileCount / this.yAxisTicksCount);
        for (let i = 0; i <= this.yAxisTicksCount; i++) {
          ticks.push(i * step);
        }
        return ticks;
      }
    },
    methods: {
      getBarHeight(fileCount) {
        // Максимальная высота 250px
        return (fileCount / this.maxFileCount) * 250;
      },
      getPercentage(fileCount) {
        return ((fileCount / this.totalFiles) * 100).toFixed(1);
      },
      onBarClick(project) {
        this.selectedProject = project;
        this.$emit('project-selected', project);
      }
    }
  };
  </script>
  
  <style scoped>
  .histogram-container {
    margin: 20px 0;
    padding: 25px;
    background: white;
    border-radius: 8px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.05);
  }
  
  .header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
    margin-right: 220px;
    flex-wrap: wrap;
    gap: 20px;
  }
  
  .stats-summary {
    display: flex;
    gap: 25px;
    background: #f8f8f8;
    padding: 15px;
    border-radius: 8px;
  }
  
  .stat-item {
    display: flex;
    flex-direction: column;
    align-items: center;
  }
  
  .stat-value {
    font-size: 1.5em;
    font-weight: bold;
    color: #292961;
  }
  
  .stat-label {
    font-size: 0.8em;
    color: #666;
  }
  
  .histogram-wrapper {
    display: flex;
    margin-top: 20px;
  }
  
  .y-axis {
    display: flex;
    flex-direction: column-reverse;
    justify-content: space-between;
    height: 250px;
    margin-right: 10px;
    width: 40px;
  }
  
  .y-tick {
    display: flex;
    align-items: center;
    position: relative;
    height: 0;
  }
  
  .tick-value {
    position: absolute;
    right: 5px;
    transform: translateY(-50%);
    font-size: 0.8em;
    color: #666;
  }
  
  .tick-line {
    position: absolute;
    left: 35px;
    right: 0;
    height: 1px;
    background: #eee;
    width: 100vw;
  }
  
  .histogram {
    display: flex;
    height: 250px;
    align-items: flex-end;
    gap: 15px;
    padding-top: 20px;
    flex: 1;
    overflow-x: auto;
    padding-bottom: 20px;
  }
  
  .bar-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    flex: 1;
    min-width: 60px;
    position: relative;
  }
  
  .bar {
    width: 40px;
    background-color: #292961;
    transition: height 0.5s ease;
    border-radius: 4px 4px 0 0;
    cursor: pointer;
    position: relative;
  }
  
  .bar:hover {
    background-color: #3a3a7a;
    opacity: 0.9;
  }
  
  .bar-tooltip {
    position: absolute;
    top: -40px;
    background: rgba(0, 0, 0, 0.8);
    color: white;
    padding: 5px 10px;
    border-radius: 4px;
    font-size: 0.8em;
    white-space: nowrap;
    visibility: hidden;
    opacity: 0;
    transition: opacity 0.2s;
    z-index: 10;
  }
  
  .bar-container:hover .bar-tooltip {
    visibility: visible;
    opacity: 1;
  }
  
  .value-label {
    margin-top: 5px;
    font-weight: bold;
    color: #292961;
  }
  
  .label {
    margin-top: 5px;
    font-size: 0.8em;
    text-align: center;
    word-break: break-word;
    max-width: 80px;
    color: #555;
  }
  
  .legend {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: 20px;
    padding-top: 20px;
    border-top: 1px solid #eee;
    flex-wrap: wrap;
    gap: 15px;
  }
  
  .legend-item {
    display: flex;
    align-items: center;
    gap: 8px;
  }
  
  .legend-color {
    width: 15px;
    height: 15px;
    border-radius: 3px;
  }
  
  .selected-project {
    background: #f0f0ff;
    padding: 8px 12px;
    border-radius: 4px;
    font-size: 0.9em;
  }
  
  @media (max-width: 768px) {
    .header {
      flex-direction: column;
      align-items: flex-start;
    }
    
    .stats-summary {
      width: 100%;
      justify-content: space-around;
    }
    
    .histogram {
      gap: 8px;
    }
    
    .bar-container {
      min-width: 40px;
    }
  }
  </style>