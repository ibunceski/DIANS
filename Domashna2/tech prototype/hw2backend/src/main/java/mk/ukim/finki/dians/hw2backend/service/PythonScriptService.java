package mk.ukim.finki.dians.hw2backend.service;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

import java.io.BufferedReader;
import java.io.File;
import java.io.InputStreamReader;
import java.io.IOException;

@Service
public class PythonScriptService {

    @Value("${python.executable}")
    private String pythonExecutable;

    @Value("${python.script.path}")
    private String scriptPath;

    @Value("${python.working.directory}")
    private String workingDirectory;

    public void executePythonScript() {
        try {
            ProcessBuilder processBuilder = new ProcessBuilder(pythonExecutable, scriptPath);
            processBuilder.directory(new File(workingDirectory));
            processBuilder.redirectErrorStream(true);

            Process process = processBuilder.start();
            String output = captureProcessOutput(process);
            int exitCode = process.waitFor();

            if (exitCode == 0) {
                System.out.println(output);
            } else {
                System.err.println("Error executing script. Exit code: " + exitCode + "\n" + output);
            }
        } catch (IOException | InterruptedException e) {
            System.err.println("Error executing Python script: " + e.getMessage());
        }
    }

    private String captureProcessOutput(Process process) throws IOException {
        BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream()));
        StringBuilder output = new StringBuilder();
        String line;
        while ((line = reader.readLine()) != null) {
            output.append(line).append("\n");
        }
        return output.toString();
    }
}

