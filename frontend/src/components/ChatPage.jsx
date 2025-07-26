import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { MessageSquare, Bot, Send } from "lucide-react";

export default function ChatPage() {
    return (
        <div className="flex flex-col items-center justify-center min-h-[80vh]">
            <Card className="w-full max-w-3xl">
                <CardHeader className="bg-green-500 rounded-t-lg">
                    <CardTitle className="flex items-center gap-2 text-white">
                        <MessageSquare className="w-6 h-6" />
                        Financial Genie Chat
                    </CardTitle>
                </CardHeader>
                <CardContent className="bg-white">
                    <div className="mb-4">
                        <div className="flex items-center gap-2 mb-2">
                            <Bot className="w-4 h-4 text-gray-500" />
                            <Badge variant="secondary">Greeter</Badge>
                        </div>
                        <div className="bg-gray-50 rounded-lg p-4 shadow text-gray-800">
                            Hello! I'm your Financial Genie. I can help you process receipts, analyze documents, answer financial questions, and create wallet passes. What would you like to do today?
                            <div className="text-xs text-gray-400 mt-2">4:59:35 PM</div>
                        </div>
                    </div>
                    <div className="flex flex-col gap-2">
                        <Input placeholder="Ask about finances, upload receipts, or get insights..." className="mb-2" />
                        <div className="flex gap-2">
                            <Button variant="outline" className="flex-1">
                                <span role="img" aria-label="calculator">🧮</span> Ask about ETFs
                            </Button>
                            <Button variant="outline" className="flex-1">
                                <span role="img" aria-label="receipt">🧾</span> Process Receipt
                            </Button>
                            <Button variant="outline" className="flex-1">
                                <span role="img" aria-label="query">⬆️</span> Query Documents
                            </Button>
                            <Button variant="success" size="icon">
                                <Send className="w-4 h-4" />
                            </Button>
                        </div>
                    </div>
                </CardContent>
            </Card>
        </div>
    );
} 