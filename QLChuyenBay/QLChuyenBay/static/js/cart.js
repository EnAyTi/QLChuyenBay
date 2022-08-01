function addToCart(mave, machuyenbay, gia) {
    event.preventDefault()

    fetch('/api/add-to-cart', {
        method: 'post',
        body: JSON.stringify({
            'mave': mave,
            'machuyenbay': machuyenbay,
            'gia': gia
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(function(res) {
        console.res
        return res.json()
    }).then(function(data) {
        console.info(data)
        let counter = document.getElementById('cart-info')
        counter.innerText = data.total_amount
    }).catch(function(err){
        console.error(err)
    })
}

function deleteCart(mave) {
    if (confirm("Bạn chắc chắn xoá vé này không?") == true) {
        fetch('/api/cart/' + mave, {
            method: 'delete',
            headers: {
                'Content-Type': 'application/json'
            }
        }).then(function(res) {
            return res.json()
        }).then(function(data) {
            let info = document.getElementsByClassName('cart-info')
            for (let i = 0; i < info.length; i++)
                info[i].innerText = data.total_quantity

            let amount = document.getElementById('amountId')
            amount.innerText = new Intl.NumberFormat().format(data.total_amount)

            let p = document.getElementById('ve' + mave)
            p.style.display = 'none'
        }).catch(function(err) {
            console.error(err)
        })
    }

}

function pay(){
    if (confirm('Xác nhận thanh toán?') == true) {
        fetch('/api/pay', {
            method: 'post'
        }).then(function(res) {
            return res.json()
        }).then(function(data) {
            console.info(data)
            if (data.code == 200)
                location.reload()
        }).catch(function(err) {
            console.error(err)
        })
    }
}
