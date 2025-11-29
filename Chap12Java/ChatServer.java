import java.io.*;
import java.net.*;
import java.util.List;
import java.util.concurrent.CopyOnWriteArrayList;

public class ChatServer {

    private final int port;
    // 동시성 안전한 리스트 사용
    private final List<ClientHandler> clients = new CopyOnWriteArrayList<>();

    public ChatServer(int port) {
        this.port = port;
    }

    public void start() throws IOException {
        ServerSocket serverSocket = new ServerSocket(port);
        System.out.println("[SERVER] Listening on port " + port);

        while (true) {
            Socket clientSocket = serverSocket.accept();
            ClientHandler handler = new ClientHandler(this, clientSocket);
            clients.add(handler);
            new Thread(handler).start();
        }
    }

    // 모든 클라이언트에게 메시지 보내기
    public void broadcast(String message) {
        String msgWithNewLine = message + "\n";
        for (ClientHandler handler : clients) {
            handler.send(msgWithNewLine);
        }
    }

    // 연결이 끊긴 클라이언트 제거
    public void removeClient(ClientHandler handler) {
        clients.remove(handler);
    }

    public static void main(String[] args) {
        int port = 5001;
        if (args.length > 0) {  // 인자로 포트 변경 가능
            port = Integer.parseInt(args[0]);
        }
        ChatServer server = new ChatServer(port);
        try {
            server.start();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}

// ---- 클라이언트 한 명을 담당하는 쓰레드 ----
class ClientHandler implements Runnable {

    private final ChatServer server;
    private final Socket socket;
    private BufferedReader in;
    private BufferedWriter out;

    public ClientHandler(ChatServer server, Socket socket) {
        this.server = server;
        this.socket = socket;
        try {
            this.in = new BufferedReader(
                    new InputStreamReader(socket.getInputStream(), "UTF-8"));
            this.out = new BufferedWriter(
                    new OutputStreamWriter(socket.getOutputStream(), "UTF-8"));
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public void send(String message) {
        try {
            out.write(message);
            out.flush();
        } catch (IOException e) {
            // 전송 실패 → 무시 (나중에 run()에서 정리됨)
        }
    }

    @Override
    public void run() {
        InetSocketAddress addr = (InetSocketAddress) socket.getRemoteSocketAddress();
        String clientInfo = addr.toString();
        System.out.println("[+] Connected: " + clientInfo);
        server.broadcast("[SYSTEM] " + clientInfo + " 입장");

        try {
            String line;
            while ((line = in.readLine()) != null) {
                if ("/quit".equals(line.trim())) {
                    break;
                }
                server.broadcast("[" + clientInfo + "] " + line);
            }
        } catch (IOException e) {
            // 통신 중 오류 → 어차피 종료 처리로 감
        } finally {
            server.broadcast("[SYSTEM] " + clientInfo + " 퇴장");
            server.removeClient(this);
            try {
                socket.close();
            } catch (IOException e) {
                // 무시
            }
            System.out.println("[-] Disconnected: " + clientInfo);
        }
    }
}
