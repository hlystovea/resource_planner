const lineChartConfig = {
  type: 'bar',
  data: {
    labels: [],
    datasets: [{
      label: 'Количество дефектов, шт.',
      data: [],
      backgroundColor: 'rgba(255, 159, 64, 0.2)',
      borderColor: 'rgba(255, 159, 64, 1)'
    }]
  },
  options: {
    elements: {
      bar: {
        borderWidth: 1,
      }
    },
    responsive: true,
    plugins: {
      legend: {
        position: 'bottom',
        labels: {
            boxHeight: 0,
        }
      }
    }
  }
};

const barChartConfig = {
  type: 'bar',
  data: {
    labels: [],
    datasets: [{
        label: 'Количество дефектов, шт.',
        data: [],
        backgroundColor: 'rgba(54, 162, 235, 0.2)',
        borderColor: 'rgba(54, 162, 235, 1)'
    }]
  },
  options: {
    indexAxis: 'y',
    elements: {
      bar: {
        borderWidth: 1,
      }
    },
    responsive: true,
    plugins: {
      legend: {
        position: 'bottom',
        labels: {
            boxHeight: 0,
        }
      }
    }
  },
};
