const { createConnection, ProposedFeatures, TextDocuments, CompletionItemKind } = require('vscode-languageserver/node');
const { TextDocument } = require('vscode-languageserver-textdocument');

const connection = createConnection(ProposedFeatures.all);
const documents = new TextDocuments(TextDocument);

connection.onInitialize(() => {
    return {
        capabilities: {
            textDocumentSync: documents.syncKind,
            completionProvider: { resolveProvider: true, triggerCharacters: ['.'] }
        }
    };
});

connection.onCompletion(() => {
    return [
        { label: 'Nova.show', kind: CompletionItemKind.Method, detail: 'Print to terminal' },
        { label: 'Nova.ask.user', kind: CompletionItemKind.Method, detail: 'Get user input' },
        { label: 'Nova.ai', kind: CompletionItemKind.Class, detail: 'Neural Network Core' },
        { label: 'Nova.hack', kind: CompletionItemKind.Class, detail: 'Cyber-Warfare Arsenal' },
        { label: 'scan', kind: CompletionItemKind.Function, detail: 'Network Recon Scanner (Nmap)' },
        { label: 'ghidra', kind: CompletionItemKind.Function, detail: 'Reverse Engineering Suite' }
    ];
});

documents.listen(connection);
connection.listen();

// [NOVA CORE INJECTION] Injecting all 200+ tools into Auto-completion
const hackerTools = ["scan","nmap","masscan","shodan","zmap","rustscan","angryip","sql","sqlmap","nikto","wpscan","dirb","gobuster","nuclei","ffuf","wfuzz","commix","brute","hydra","medusa","ncrack","hash","hashcat","john","patator","kerbrute","shark","wireshark","ettercap","mitmproxy","tcpdump","responder","bettercap","msf","metasploit","searchsploit","nc","netcat","cobaltstrike","empire","sliver","air","aircrack","wifite","kismet","reaver","pixie","airgeddon","ghidra","radare2","jadx","apktool","binwalk","autopsy","steghide","theHarvester","maltego","amass","subfinder","mimikatz","crackmapexec","chisel","ngrok"];

connection.onCompletion((_textDocumentPosition) => {
    let suggestions = [
        { label: 'Nova.show', kind: CompletionItemKind.Method, detail: 'Silicon Core Print' },
        { label: 'Nova.ask.user', kind: CompletionItemKind.Method, detail: 'Silicon Core Input' },
        { label: 'Nova.ai', kind: CompletionItemKind.Class, detail: 'Neural Engine' },
        { label: 'Nova.hack', kind: CompletionItemKind.Class, detail: 'Cyber-Warfare Core' }
    ];
    
    // Dynamically adding all tools
    hackerTools.forEach(tool => {
        suggestions.push({ label: tool, kind: CompletionItemKind.Function, detail: 'Nova Hacker Arsenal' });
    });
    
    return suggestions;
});
