import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Upload, Image } from "lucide-react";

export default function UploadPage() {
    return (
        <div className="flex flex-col items-center justify-center min-h-[80vh]">
            <Card className="w-full max-w-3xl border-2 border-dashed border-green-300 bg-white/50 shadow-none">
                <CardHeader className="text-center">
                    <CardTitle className="flex items-center justify-center gap-2 text-2xl">
                        <Upload className="w-6 h-6" />
                        Upload Receipt Images
                    </CardTitle>
                    <CardDescription>
                        Drag and drop receipt images or click to browse. Supports JPG and PNG formats.
                    </CardDescription>
                </CardHeader>
                <CardContent>
                    <div className="flex flex-col items-center justify-center border-2 border-dashed border-gray-300 rounded-xl py-10 bg-white/80">
                        <div className="bg-green-500 rounded-full p-4 mb-4">
                            <Image className="w-8 h-8 text-white" />
                        </div>
                        <div className="text-lg font-semibold mb-1">Upload receipt images</div>
                        <div className="text-gray-500 mb-4">or click to browse from your device</div>
                        <Button variant="success" className="px-8 py-2">
                            <Upload className="w-4 h-4 mr-2" />
                            Select Files
                        </Button>
                    </div>
                </CardContent>
            </Card>
        </div>
    );
} 