document.addEventListener('DOMContentLoaded', function () {
    const totalOrders = document.getElementById('total_orders');
    const activeUsers = document.getElementById('active_users');
    const paidOrders = document.getElementById('paid_orders');
    const newOrders = document.getElementById('new_orders');

    const btnOrders = document.getElementById('btn_all_orders');
    const btnUsers = document.getElementById('btn_users');
    const btnPaid = document.getElementById('btn_paid_orders');
    const btnNewOrders = document.getElementById('btn_new_orders');
    const seenUrl = btnNewOrders.dataset.url;

    function hideAll() {
        totalOrders.classList.add('hidden');
        activeUsers.classList.add('hidden');
        paidOrders.classList.add('hidden');
        newOrders.classList.add('hidden');

    }
    
    btnNewOrders.addEventListener('click', function () {
        hideAll();
        newOrders.classList.remove('hidden');
        fetch(seenUrl)
    })
    
    btnOrders.addEventListener('click', function () {
        hideAll();
        totalOrders.classList.remove('hidden');
    })

    btnUsers.addEventListener('click', function(){
        hideAll();
        activeUsers.classList.remove('hidden');
    })

    btnPaid.addEventListener('click', function(){
        hideAll()
        paidOrders.classList.remove('hidden');
    })
})
