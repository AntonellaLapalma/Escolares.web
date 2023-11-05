var ctx = document.getElementById('graficoDeBarrasIngreso').getContext('2d');
var datos_ingreso = JSON.parse(document.getElementById('datos_ingreso').value);

                
                var data = {
                    labels: ['Ene','Feb','Mar','Abr', 'May','Jun','Jul','Ago','Sep','Oct','Nov','Dic'],
                    datasets: [{
                        label: 'Total facturado',
                        data: datos_ingreso,
                        backgroundColor: '#ff7700',
                        borderColor: '#ff7700',
                        borderWidth: 1
                    }]
                };
            
                var config = {
                    type: 'bar',
                    data: data,
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        scales: {
                            y: {
                                beginAtZero: true
                            }
                        }
                    }
                };
                var myChart = new Chart(ctx, config);

var ctx2 = document.getElementById('graficoDeBarrasGastos').getContext('2d');
var datos_gastos = JSON.parse(document.getElementById('datos_gastos').value);
                
                var data2 = {
                    labels: ['Ene','Feb','Mar','Abr', 'May','Jun','Jul','Ago','Sep','Oct','Nov','Dic'],
                    datasets: [{
                        label: 'Total gastado',
                        data: datos_gastos,
                        backgroundColor: '#ff7700',
                        borderColor: '#ff7700',
                        borderWidth: 1
                    }]
                };
                
                var config2 = {
                    type: 'bar',
                    data: data2,
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        scales: {
                            y: {
                                beginAtZero: true
                            }
                        }
                    }
                };
                
                var myChart2 = new Chart(ctx2, config2);