// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional

///datn link
var firebaseConfig = {
    apiKey: "AIzaSyAeSga_8XW4IBgkChstFgOeFgL-99FFS_w",
    authDomain: "tomatoproject-b1282.firebaseapp.com",
    databaseURL: "https://tomatoproject-b1282-default-rtdb.firebaseio.com",
    projectId: "tomatoproject-b1282",
    storageBucket: "tomatoproject-b1282.appspot.com",
    messagingSenderId: "775581346986",
     appId: "1:775581346986:web:6823c2e0fff08e16a2f4d3"
};

// Initialize Firebase
firebase.initializeApp(firebaseConfig);

///doi form submit de goi ham submit
document.getElementById('Form').addEventListener('submit', submitForm);

///ham submit
function submitForm(e) {
    e.preventDefault(); // ngan khong cho gui du lieu di mat

    //lay gia tri cac o
    var x = document.getElementById("Loai").value;
    const min = document.getElementById("min").value;
    const max = document.getElementById("max").value;
    var RED = document.getElementById("red").checked;
    var ORANGE = document.getElementById("orange").checked;
    var GREEN = document.getElementById("green").checked;

    ///so sanh max min
    if (Number(max) < Number(min))
    {
        ///thong bao maxx min nhap sai
        alertCustom('brown', 'Max Min không đúng');
    }
    else
    {
        ///ghi database
        var fbase = firebase.database().ref(x);
        fbase.set({
            min: min,
            max: max,
            RED: RED,
            ORANGE: ORANGE,
            GREEN: GREEN

        });

        ///xoa form
        document.getElementById("Form").reset();
        ///hien thi thong bao thanh cong
        alertCustom('#4CAF50', 'Đã lưu thông tin');

        location.reload();
    }
}

///ham tuy chinh thong bao
function alertCustom(color, mess) {
    ///hien thi thong bao
    document.querySelector('.alert').style.display = 'block';
    document.querySelector('.alert').style.background = color;
    document.getElementById('alert').innerHTML = mess;

    ///thong bao tu tat sau 2 giay
    setTimeout(function () {
        document.querySelector('.alert').style.display = 'none';
    }, 2000);
}

function addItemToList(type,green, orange, red, min ,max)
{
    var ul = document.getElementById('list');
    var _header = document.createElement('h4');
    var _red = document.createElement('li');
    var _orange = document.createElement('li');
    var _green = document.createElement('li');
    var _min = document.createElement('li');
    var _max = document.createElement('li');

    _header.innerHTML = "Loại: " + type;
    _green.innerHTML = "Green: " + green;
    _orange.innerHTML = "Orange: " + orange;
    _red.innerHTML = "Red: " + red;
    _min.innerHTML = "Min: " + min;
    _max.innerHTML = "Max: " + max;

    ul.appendChild(_header);
    ul.appendChild(_red);
    ul.appendChild(_orange);
    ul.appendChild(_green);
    ul.appendChild(_min);
    ul.appendChild(_max);

}

stdNo = 0
function getServerData()
{
    firebase.database().ref().once('value', function(snapshot){
        snapshot.forEach(
            function(ChildSnapshot){
                let green = ChildSnapshot.val().GREEN;
                let orange =  ChildSnapshot.val().ORANGE;
                let red = ChildSnapshot.val().RED;
                let min =  ChildSnapshot.val().min;
                let max = ChildSnapshot.val().max;
                
                console.log(stdNo);
                if (stdNo != 0)
                {
                    addItemToList(stdNo,green, orange, red, min, max);
                }
                stdNo = stdNo + 1
            }
        );
    });
}

window.onload = getServerData;