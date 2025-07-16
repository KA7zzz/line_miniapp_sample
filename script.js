// DOMが読み込まれたら実行
document.addEventListener('DOMContentLoaded', () => {
    // LIFFを初期化する
    liff.init({
        liffId: "2007763153" // 1. ここをあなたのLIFF IDに書き換える
    })
    .then(() => {
        // ログインしているかチェック
        if (!liff.isLoggedIn()) {
            liff.login(); // ログインしていなければ、ログインさせる
        }
    })
    .catch((err) => {
        console.error('LIFF Initialization failed', err);
    });

    // ボタンにクリックイベントを設定
    const recordButton = document.getElementById('record-button');
    recordButton.addEventListener('click', recordVisit);
});

// バックエンドAPIを呼び出す非同期関数
async function recordVisit() {
    try {
        // メッセージ表示欄をクリア
        document.getElementById('message').innerText = "通信中...";

        // LINEプロフィールを取得してユーザーIDを得る
        const profile = await liff.getProfile();
        
        // RenderでデプロイしたバックエンドのURL
        const FLASK_APP_URL = 'https://line-miniapp-sample.onrender.com/record-visit'; // 2. ここをあなたのRenderのURLに書き換える

        // fetch APIを使ってバックエンドにPOSTリクエストを送信
        const response = await fetch(FLASK_APP_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                lineUserId: profile.userId,
                memo: "ミニアプリからの訪問！" 
            }),
        });

        // レスポンスが正常でない場合はエラーを投げる
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || 'サーバーエラーが発生しました。');
        }

        // 成功メッセージを取得して表示
        const result = await response.json();
        document.getElementById('message').innerText = result.message;
        alert(result.message);

    } catch (error) {
        console.error('API呼び出しエラー:', error);
        document.getElementById('message').innerText = 'エラーが発生しました。';
        alert('エラーが発生しました: ' + error.message);
    }
}