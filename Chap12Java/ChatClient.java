import java.io.*;
import java.net.Socket;
import java.util.Scanner;

public class ChatClient {

    private final String host;
    private final int port;
    private Socket socket;
    private BufferedReader in;
    private BufferedWriter out;

    public ChatClient(String host, int port) {
        this.host = host;
        this.port = port;
    }

    public void start() throws IOException {
        socket = new Socket(host, port);
        in = new BufferedReader(
                new InputStreamReader(socket.getInputStream(), "UTF-8"));
        out = new BufferedWriter(
                new OutputStreamWriter(socket.getOutputStream(), "UTF-8"));

        System.out.println("[SYSTEM] 서버에 연결되었습니다. (/quit 입력 시 종료)");

        // 수신 쓰레드
        Thread recvThread = new Thread(this::recvLoop);
        recvThread.setDaemon(true);
        recvThread.start();

        // 송신 루프 (메인 쓰레드)
        sendLoop();
    }

    private void recvLoop() {
        try {
            String line;
            while ((line = in.readLine()) != null) {
                System.out.println(line);
            }
        } catch (IOException e) {
            // 무시
        } finally {
            System.out.println("[SYSTEM] 서버 연결 종료");
        }
    }

    private void sendLoop() {
        Scanner scanner = new Scanner(System.in);
        try {
            while (true) {
                String msg = scanner.nextLine();
                out.write(msg);
                out.write("\n");
                out.flush();

                if ("/quit".equals(msg.trim())) {
                    break;
                }
            }
        } catch (IOException e) {
            // 무시
        } finally {
            try {
                socket.close();
            } catch (IOException e) {
                // 무시
            }
            scanner.close();
        }
    }

    public static void main(String[] args) {
        String host = "127.0.0.1";
        int port = 5001;

        if (args.length >= 1) host = args[0];
        if (args.length >= 2) port = Integer.parseInt(args[1]);

        ChatClient client = new ChatClient(host, port);
        try {
            client.start();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
