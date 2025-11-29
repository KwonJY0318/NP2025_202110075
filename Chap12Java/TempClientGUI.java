// TempClientGUI.java
import java.awt.*;
import java.awt.event.ActionEvent;
import java.io.*;
import java.net.Socket;
import javax.swing.*;

public class TempClientGUI extends JFrame {

    private JTextField tfInput;
    private JLabel lbResult;
    private JRadioButton rbCtoF, rbFtoC;

    private final String host;
    private final int port;

    public TempClientGUI(String host, int port) {
        this.host = host;
        this.port = port;
        initUI();
    }

    private void initUI() {
        setTitle("Temperature Converter");
        setSize(400, 200);
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setLocationRelativeTo(null);

        tfInput = new JTextField(10);
        lbResult = new JLabel("Result: ");

        rbCtoF = new JRadioButton("C → F", true);
        rbFtoC = new JRadioButton("F → C");
        ButtonGroup group = new ButtonGroup();
        group.add(rbCtoF);
        group.add(rbFtoC);

        JButton btnConvert = new JButton(new AbstractAction("Convert") {
            @Override
            public void actionPerformed(ActionEvent e) {
                convertTemperature();
            }
        });

        JPanel panel = new JPanel(new GridLayout(4, 1));

        JPanel p1 = new JPanel();
        p1.add(new JLabel("Temperature:"));
        p1.add(tfInput);

        JPanel p2 = new JPanel();
        p2.add(rbCtoF);
        p2.add(rbFtoC);

        JPanel p3 = new JPanel();
        p3.add(btnConvert);

        JPanel p4 = new JPanel();
        p4.add(lbResult);

        panel.add(p1);
        panel.add(p2);
        panel.add(p3);
        panel.add(p4);

        add(panel);
    }

    private void convertTemperature() {
        String value = tfInput.getText().trim();
        if (value.isEmpty()) {
            JOptionPane.showMessageDialog(this, "값을 입력하세요");
            return;
        }

        String request = rbCtoF.isSelected() ? "C:" + value : "F:" + value;

        try (Socket socket = new Socket(host, port);
             BufferedReader in = new BufferedReader(
                     new InputStreamReader(socket.getInputStream(), "UTF-8"));
             BufferedWriter out = new BufferedWriter(
                     new OutputStreamWriter(socket.getOutputStream(), "UTF-8"))) {

            out.write(request + "\n");
            out.flush();

            String resp = in.readLine();
            lbResult.setText("Result: " + resp);

        } catch (IOException e) {
            JOptionPane.showMessageDialog(this, "서버 연결 실패: " + e.getMessage());
        }
    }

    public static void main(String[] args) {
        String host = "127.0.0.1";
        int port = 6000;

        if (args.length >= 1) host = args[0];
        if (args.length >= 2) port = Integer.parseInt(args[1]);

        // 🔹 람다에서 사용할 final 변수로 복사
        final String finalHost = host;
        final int finalPort = port;

        SwingUtilities.invokeLater(() -> {
            TempClientGUI gui = new TempClientGUI(finalHost, finalPort);
            gui.setVisible(true);
        });
    }
}
