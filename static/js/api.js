//detailchart
const renderdetailChart=(sources,amount) => {
    var ctx = document.getElementById('details').getContext('2d');
    var detailChart = new Chart(ctx, {
        type: 'bar',
        //data_start
        data: {
            labels:sources,
            datasets: [{
                label: sources,
                data:amount,
                backgroundColor: [
                    'rgba(255, 99, 132, 0.5)','rgba(54, 162, 235, 0.5)','rgba(255, 206, 86, 0.5)'                              
                ],
                borderColor: [
                    'rgba(255, 99, 132, 1)','rgba(54, 162, 235, 1)','rgba(255, 206, 86, 1)'                              
                ],
                borderWidth: 2
            }]
          },
            //data_end,option_start
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
            maintainAspectRatio:false,
            scales: {
                  yAxes: [{
                      ticks: {
                          beginAtZero: true
                      }
                  }]
              }
           }//option_end                
    }
);
}

const renderexpenseChart=(category,expense) => {
var ctx = document.getElementById('expenseChart').getContext('2d');
var detailChart = new Chart(ctx, {
  type: 'doughnut',
  data: {
      labels:category,
      datasets: [{
          label: 'Expense Detail',
          data:expense,
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
      
      responsive:true,
      maintainAspectRatio:false
      
  },                
});
}

const renderincomeChart=(source,incomes) => {
var ctx = document.getElementById('incomeChart').getContext('2d');
var detailChart = new Chart(ctx, {
type: 'doughnut',
data: {
  labels:source,
  datasets: [{
      label: 'Income Detail',
      data:incomes,
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
  
  responsive:true,
  maintainAspectRatio:false
  
},                
});
}

const getapidata=()=>{
var date = document.getElementById('from_date').value;
console.log('date',date)
fetch('{% url 'dashboardapi' %}').then(res=>res.json())
.then((apidata)=>{
console.log('data',apidata)
const data=apidata.detail_dict;
const [sources,amount]=[Object.keys(data),Object.values(data)]
//   var l = sources.length
console.log('sources',sources)
console.log('amount',amount)

const data2=apidata.expenses;
const [category,expense]=[Object.keys(data2),Object.values(data2)]
console.log('category',category)
console.log('amount',expense)

const data3=apidata.income;
const [source,incomes]=[Object.keys(data3),Object.values(data3)]
console.log('source',source)
console.log('amount',incomes)

renderdetailChart(sources,amount);
renderincomeChart(source,incomes);
renderexpenseChart(category,expense);
});
};



document.onload=getapidata();