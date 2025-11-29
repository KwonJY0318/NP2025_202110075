// TempServer.java
import java.io.*;
import java.net.*;

public class TempServer {

    private final int port;

    public TempServer(int port) {
        this.port = port;
    }

    public void start() throws IOException {
        ServerSocket serverSocket = new ServerSocket(port);
        System.out.println("[TempServer] Listening on port " + port);

        while (true) {
            Socket clientSocket = serverSocket.accept();
            System.out.println("[+] Client connected: " + clientSocket.getRemoteSocketAddress());
            new Thread(() -> handleClient(clientSocket)).start();
        }
    }

    private void handleClient(Socket socket) {
        try (BufferedReader in = new BufferedReader(
                 new InputStreamReader(socket.getInputStream(), "UTF-8"));
             BufferedWriter out = new BufferedWriter(
                 new OutputStreamWriter(socket.getOutputStream(), "UTF-8"))) {

            String line;
            while ((line = in.readLine()) != null) {
                String result = convertTemperature(line.trim());
                out.write(result + "\n");
                out.flush();
            }
        } catch (IOException e) {
            System.out.println("[!] Client disconnected");
        } finally {
            try { socket.close(); } catch (IOException e) {}
        }
    }

    private String convertTemperature(String msg) {
        try {
            if (msg.startsWith("C:")) {
                double c = Double.parseDouble(msg.substring(2));
                double f = c * 9.0 / 5.0 + 32.0;
                return "F: " + String.format("%.2f", f);

            } else if (msg.startsWith("F:")) {
                double f = Double.parseDouble(msg.substring(2));
                double c = (f - 32.0) * 5.0 / 9.0;
                return "C: " + String.format("%.2f", c);
            }
        } catch (NumberFormatException e) {
            return "ERROR: invalid number";
        }

        return "ERROR: invalid format (예: C:25 또는 F:77)";
    }

    public static void main(String[] args) {
        int port = 6000;
        if (args.length > 0) port = Integer.parseInt(args[0]);

        TempServer server = new TempServer(port);
        try {
            server.start();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
