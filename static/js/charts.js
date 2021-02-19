const renderdetailChart=(amount,sources) => {
              var ctx = document.getElementById('details').getContext('2d');
              var detailChart = new Chart(ctx, {
                  type: 'doughnut',
                  data: {
                      labels:sources,
                      datasets: [{
                          label: 'Money Detail',
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
                        text:'Money Details'
                      },
                      legend:{
                          display:true,
                          text:'Money Detail',
                          position:'bottom',
                          align:'center'                     
                        

                      },
                      responsive:true,
                      maintainAspectRatio:false
                      
                  },                
              });
      }

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