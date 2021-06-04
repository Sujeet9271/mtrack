

const renderexpenseChart=(amount,category) => {
        var ctx = document.getElementById('expenseChart').getContext('2d');
        var detailChart = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels:category,
                datasets: [{
                    label: 'Expense Detail',
                    data:amount,
                    backgroundColor: [
                        'rgba(255, 99, 132, 0.5)',
                        'rgba(54, 162, 235, 0.5)',
                        'rgba(255, 206, 86, 0.5)',
                        'rgba(75, 192, 192, 0.5)',
                        'rgba(153, 102, 255, 0.5)',
                        'rgba(255, 159, 64, 0.5)'
                    ],
                    borderColor: [
                        'rgba(255, 99, 132, 1)',
                        'rgba(54, 162, 235, 1)',
                        'rgba(255, 206, 86, 1)',
                        'rgba(75, 192, 192, 1)',
                        'rgba(153, 102, 255, 1)',
                        'rgba(255, 159, 64, 1)'
                    ],
                    borderWidth: 2
                }]
            },
            options: {
                title:{
                  display:true,
                  text:'Expenses Detail'
                },
                legend:{
                    display:true,
                    text:'Expense Detail',
                    position:'bottom',
                    align:'center'                     
                  

                },
                responsive:true,
                maintainAspectRatio:false
                
            },                
        });
}

const renderincomeChart=(amount,source) => {
    var ctx = document.getElementById('incomeChart').getContext('2d');
    var detailChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels:source,
            datasets: [{
                label: 'Income Detail',
                data:amount ,
                backgroundColor: [
                    'rgba(255, 99, 132, 0.5)',
                    'rgba(54, 162, 235, 0.5)',
                    'rgba(255, 206, 86, 0.5)',
                    'rgba(75, 192, 192, 0.5)',
                    'rgba(153, 102, 255, 0.5)',
                    'rgba(255, 159, 64, 0.5)'
                ],
                borderColor: [
                    'rgba(255, 99, 132, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(153, 102, 255, 1)',
                    'rgba(255, 159, 64, 1)'
                ],
                borderWidth: 2
            }]
        },
        options: {
            title:{
              display:true,
              text:'Income Detail'
            },
            legend:{
                display:true,
                text:'Income Detail',
                position:'bottom',
                align:'center'                     
              

            },
            responsive:true,
            maintainAspectRatio:false
            
        },                
    });
}






const renderdetailChart=(expense_label,expense_data,income_data,income_label,savings_data,savings_label) => {
  var ctx = document.getElementById('details').getContext('2d');
  var detailChart = new Chart(ctx, {
      type: 'doughnut',
      data: details,
      options: chartOptions
    })
 
  var income = {
      label: 'income',
      data: income_data,
      backgroundColor: 'green',
      borderWidth: 0,
      yAxisID: "y-axis-density"
    };
    
  var expense = {
      label: 'expense',
      data: expense_data,
      backgroundColor: 'red',
      borderWidth: 0,
      yAxisID: "y-axis-gravity"
    };
    
  var savings = {
      label: 'savings',
      data: savings_data,
      backgroundColor: 'yellow',
      borderWidth: 0,
      yAxisID: "y-axis-gravity"
    };
    
  var details = {
      labels: ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"],
      datasets: [income,expense,savings]
    };
    
  var chartOptions = {
      scales: {
        xAxes: [{
          barPercentage: 1,
          categoryPercentage: 0.6
        }],
        yAxes: [{
          id: "y-axis-density"
        }, {
          id: "y-axis-gravity"
        }]
      }
    };
    
  };



//exp
  const renderdetailChart=(expense_label,expense_data,income_data,income_label,savings_data,savings_label) => {
    var ctx = document.getElementById('details').getContext('2d');
    var detailChart = new Chart(ctx, {
        type: 'doughnut',
        data: details,
        options: chartOptions
      })
   
    var income = {
        label: 'income',
        data: income_data,
        backgroundColor: 'green',
        borderWidth: 0,
        yAxisID: "y-axis-density"
      };
      
    var expense = {
        label: 'expense',
        data: expense_data,
        backgroundColor: 'red',
        borderWidth: 0,
        yAxisID: "y-axis-gravity"
      };
      
    var savings = {
        label: 'savings',
        data: savings_data,
        backgroundColor: 'yellow',
        borderWidth: 0,
        yAxisID: "y-axis-gravity"
      };
      
    var details = {
        labels: ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"],
        datasets: [income,expense,savings]
      };
      
    var chartOptions = {
        scales: {
          xAxes: [{
            barPercentage: 1,
            categoryPercentage: 0.6
          }],
          yAxes: [{
            id: "y-axis-density"
          }, {
            id: "y-axis-gravity"
          }]
        }
      };
      
    };
  