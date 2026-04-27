// 表示したい画像/動画SSのリスト
const contents = [
    { id: "IMG_8824", date: "2022/08/15 22:10", src: "path/to/self-defense.jpg" },
    { id: "MEM_0404", date: "2024/11/03 01:45", src: "path/to/fukami.png" },
    { id: "LOG_9901", date: "2025/12/24 23:59", src: "path/to/moderator-log.jpg" }
];

// 初期化：ランダムにコンテンツを表示
window.onload = () => {
    const data = contents[Math.floor(Math.random() * contents.length)];
    document.getElementById('val-id').innerText = data.id;
    document.getElementById('val-date').innerText = data.date;
    // 画像がある場合は以下を有効に
    // const img = document.getElementById('contentImg');
    // img.src = data.src; img.style.display = 'block';
    // document.getElementById('contentPlaceholder').style.display = 'none';
};

// ポリシーのチェックで色を濃くする
function togglePolicy(el) {
    const parent = el.closest('.policy-item');
    if(el.checked) parent.classList.add('is-active');
    else parent.classList.remove('is-active');
    document.querySelector('.btn-submit').classList.add('ready');
}

// 判定処理
function judge(type) {
    const card = document.getElementById('targetCard');
    card.classList.remove('judged-approve', 'judged-ban');
    
    if(type === 'approve') {
        card.classList.add('judged-approve');
        document.getElementById('val-status').innerText = "APPROVED";
        document.getElementById('val-status').style.color = "#2ecc71";
    } else {
        card.classList.add('judged-ban');
        document.getElementById('val-status').innerText = "BANNED";
        document.getElementById('val-status').style.color = "#e74c3c";
    }
}

function submit() {
    alert("Decision Submitted. System Synchronized.");
}