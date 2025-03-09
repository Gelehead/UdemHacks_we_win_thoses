// charts.js - Module for handling visualization of running data
class RunningAnalyticsVisualizer {
    constructor() {
      this.chartContainer = null;
      this.chartCanvas = null;
      this.videoContainer = null;
      this.comparisonContainer = null;
      this.jsonData = null;
      this.chart = null; // Store chart instance for later reference
    }
  
    /**
     * Initialize the visualizer with container references
     */
    init(chartContainerId, videoComparisonId) {
      this.chartContainer = document.getElementById(chartContainerId);
      this.comparisonContainer = document.getElementById(videoComparisonId);
      
      if (!this.chartContainer) {
        console.error("Chart container not found");
        return false;
      }
      
      if (!this.comparisonContainer) {
        console.error("Video comparison container not found");
        return false;
      }
      
      // Create canvas for the chart
      this.chartCanvas = document.createElement('canvas');
      this.chartCanvas.id = 'distanceChart';
      this.chartCanvas.width = 800;
      this.chartCanvas.height = 400;
      this.chartContainer.appendChild(this.chartCanvas);
      
      return true;
    }
  
    /**
     * Load JSON data from a file or string
     */
    loadData(jsonData) {
      try {
        this.jsonData = typeof jsonData === 'string' ? JSON.parse(jsonData) : jsonData;
        return true;
      } catch (error) {
        console.error("Error parsing JSON data:", error);
        return false;
      }
    }
  
    /**
     * Create the distance chart using the loaded data
     */
    createDistanceChart() {
      if (!this.jsonData || !this.chartCanvas) {
        console.error("No data loaded or chart canvas not initialized");
        return false;
      }
  
      try {
        const ctx = this.chartCanvas.getContext('2d');
        
        // Clear any existing chart
        this.clearChart();
        
        // Prepare the data
        const distances = this.jsonData.distances || [];
        if (distances.length === 0) {
          console.error("No distance data available");
          this.showError("No distance data available");
          return false;
        }
        
        const labels = distances.map((_, index) => index);
        const peakIndices = this.jsonData.peak_indices || [];
        
        // Create datasets
        const datasets = [
          {
            label: 'Distance',
            data: distances,
            borderColor: 'rgb(75, 192, 192)',
            backgroundColor: 'rgba(75, 192, 192, 0.2)',
            tension: 0.1,
            fill: true
          }
        ];
        
        // Create chart annotations for peak points
        const annotations = {};
        peakIndices.forEach((peakIndex, i) => {
          annotations[`peak-${i}`] = {
            type: 'point',
            xValue: peakIndex,
            yValue: distances[peakIndex],
            backgroundColor: 'red',
            radius: 5
          };
        });
  
        // Create the chart
        this.chart = new Chart(ctx, {
          type: 'line',
          data: {
            labels: labels,
            datasets: datasets
          },
          options: {
            responsive: true,
            plugins: {
              title: {
                display: true,
                text: `Running Distance Analysis (${this.jsonData.step_count} steps detected)`
              },
              tooltip: {
                callbacks: {
                  label: function(context) {
                    const index = context.dataIndex;
                    const isPeak = peakIndices.includes(index);
                    return `Distance: ${context.raw.toFixed(4)}${isPeak ? ' (STEP)' : ''}`;
                  }
                }
              },
              annotation: {
                annotations: annotations
              }
            },
            scales: {
              x: {
                title: {
                  display: true,
                  text: 'Frame'
                }
              },
              y: {
                title: {
                  display: true,
                  text: 'Distance'
                },
                beginAtZero: true
              }
            },
            interaction: {
              mode: 'index',
              intersect: false
            }
          }
        });
        
        return this.chart;
      } catch (error) {
        console.error("Error creating chart:", error);
        this.showError(`Error creating chart: ${error.message}`);
        return false;
      }
    }
    
    /**
     * Clear any existing chart
     */
    clearChart() {
      if (this.chart) {
        this.chart.destroy();
        this.chart = null;
      }
    }
    
    /**
     * Show an error message in the chart container
     */
    showError(message) {
      if (this.chartContainer) {
        const errorMsg = document.createElement('div');
        errorMsg.className = 'chart-error';
        errorMsg.style.color = 'red';
        errorMsg.style.padding = '20px';
        errorMsg.style.textAlign = 'center';
        errorMsg.textContent = message;
        
        // Clear container and add error
        this.chartContainer.innerHTML = '';
        this.chartContainer.appendChild(errorMsg);
      }
    }
  
    /**
     * Set up side-by-side video comparison
     */
    setupVideoComparison(originalVideoPath, processedVideoPath) {
      if (!this.comparisonContainer) {
        console.error("Video comparison container not initialized");
        return false;
      }
      
      // Clear existing content
      this.comparisonContainer.innerHTML = '';
      
      // Create container for the original video
      const originalContainer = document.createElement('div');
      originalContainer.className = 'video-box';
      
      // Create container for the processed video
      const processedContainer = document.createElement('div');
      processedContainer.className = 'video-box';
      
      // Create and configure the original video element
      const originalVideo = document.createElement('video');
      originalVideo.id = 'originalVideo';
      originalVideo.controls = true;
      originalVideo.width = 400;
      originalVideo.height = 300;
      originalVideo.src = originalVideoPath;
      
      // Create and configure the processed video element
      const processedVideo = document.createElement('video');
      processedVideo.id = 'processedVideo';
      processedVideo.controls = true;
      processedVideo.width = 400;
      processedVideo.height = 300;
      processedVideo.src = processedVideoPath;
      
      // Create labels for each video
      const originalLabel = document.createElement('h3');
      originalLabel.textContent = 'Original Video';
      
      const processedLabel = document.createElement('h3');
      processedLabel.textContent = 'Processed Video';
      
      // Add elements to their containers
      originalContainer.appendChild(originalLabel);
      originalContainer.appendChild(originalVideo);
      
      processedContainer.appendChild(processedLabel);
      processedContainer.appendChild(processedVideo);
      
      // Add containers to the comparison container
      this.comparisonContainer.appendChild(originalContainer);
      this.comparisonContainer.appendChild(processedContainer);
      
      // Add synchronization between videos
      originalVideo.addEventListener('play', () => {
        processedVideo.currentTime = originalVideo.currentTime;
        processedVideo.play();
      });
      
      originalVideo.addEventListener('pause', () => {
        processedVideo.pause();
      });
      
      processedVideo.addEventListener('play', () => {
        originalVideo.currentTime = processedVideo.currentTime;
        originalVideo.play();
      });
      
      processedVideo.addEventListener('pause', () => {
        originalVideo.pause();
      });
      
      // Function to sync video times
      const syncTime = (source, target) => {
        source.addEventListener('timeupdate', () => {
          // Only sync if the difference is more than 0.3 seconds
          if (Math.abs(target.currentTime - source.currentTime) > 0.3) {
            target.currentTime = source.currentTime;
          }
        });
      };
      
      syncTime(originalVideo, processedVideo);
      syncTime(processedVideo, originalVideo);
      
      return true;
    }
    
    /**
     * Load JSON data from a filepath
     */
    async loadJsonFromFile(filePath) {
      try {
        const response = await fetch(filePath);
        if (!response.ok) {
          throw new Error(`Failed to load JSON: ${response.status} ${response.statusText}`);
        }
        
        const jsonData = await response.json();
        this.loadData(jsonData);
        return true;
      } catch (error) {
        console.error("Error loading JSON file:", error);
        return false;
      }
    }
  }
  
  // Export the class so it can be used in other scripts
  window.RunningAnalyticsVisualizer = RunningAnalyticsVisualizer;