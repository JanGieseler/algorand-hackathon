import { useSnackbar } from "notistack";
import { useState, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { Dialog, DialogContent, DialogDescription, DialogFooter, DialogHeader, DialogTitle, DialogClose } from "@/components/ui/dialog";

interface VerifyContentInterface {
  openModal: boolean;
  setModalState: (value: boolean) => void;
}

interface VerifyFormData {
  content: string;
  publisher: string;
  creator: string;
  description: string;
  latitude: number;
  longitude: number;
  timestamp: string;
}

const VerifyContent = ({ openModal, setModalState }: VerifyContentInterface) => {
  const [loading, setLoading] = useState<boolean>(false);
  const [formData, setFormData] = useState<VerifyFormData>({
    content: "",
    publisher: "",
    creator: "",
    description: "",
    latitude: 0,
    longitude: 0,
    timestamp: "",
  });

  const { enqueueSnackbar } = useSnackbar();

  useEffect(() => {
    if (openModal) {
      const berlinCoordinates = {
        latitude: 52.52,
        longitude: 13.405,
      };

      if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
          (position) => {
            setFormData((prev) => ({
              ...prev,
              latitude: position.coords.latitude,
              longitude: position.coords.longitude,
            }));
          },
          () => {
            setFormData((prev) => ({
              ...prev,
              ...berlinCoordinates,
            }));
          }
        );
      } else {
        setFormData((prev) => ({
          ...prev,
          ...berlinCoordinates,
        }));
      }
    }
  }, [openModal]);

  const handleInputChange = (field: keyof VerifyFormData, value: string) => {
    setFormData((prev) => ({
      ...prev,
      [field]: value,
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);

    // Validate required fields
    if (!formData.content.trim() || !formData.publisher.trim() || !formData.creator.trim() || !formData.description.trim()) {
      enqueueSnackbar("Please fill in all fields", { variant: "warning" });
      setLoading(false);
      return;
    }

    try {
      enqueueSnackbar("Verifying content...", { variant: "info" });
      const { latitude, longitude, ...rest } = formData;
      const dataToSubmit = {
        ...rest,
        timestamp: new Date(Date.now()).toISOString(),
        location: {
          latitude: formData.latitude,
          longitude: formData.longitude,
        },
      };

      const response = await fetch("http://localhost:8000/verify", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(dataToSubmit),
      });

      if (response.ok) {
        enqueueSnackbar("Content verified successfully!", { variant: "success" });
        // Reset form
        setFormData({
          content: "",
          publisher: "",
          creator: "",
          description: "",
          latitude: 0,
          longitude: 0,
          timestamp: "",
        });
        setModalState(false);
      } else {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
    } catch (e) {
      console.error("Upload failed:", e);
      enqueueSnackbar("Failed to verify content", { variant: "error" });
    }

    setLoading(false);
  };

  const isFormValid = formData.content.trim() && formData.publisher.trim() && formData.creator.trim() && formData.description.trim();

  return (
    <Dialog open={openModal} onOpenChange={setModalState}>
      <DialogContent className="sm:max-w-[425px] bg-slate-200">
        <form onSubmit={handleSubmit}>
          <DialogHeader>
            <DialogTitle>Verify Content</DialogTitle>
            <DialogDescription>Fill out the form below to verify your content</DialogDescription>
          </DialogHeader>
          <div className="grid gap-4 py-4">
            <div className="grid gap-2">
              <Label htmlFor="content-1">Content</Label>
              <Textarea
                id="content-1"
                name="content"
                placeholder="Enter your content here..."
                required
                className="min-h-[100px]"
                value={formData.content}
                onChange={(e) => handleInputChange("content", e.target.value)}
              />
            </div>

            <div className="grid gap-2">
              <Label htmlFor="description-1">Description</Label>
              <Input
                id="description-1"
                name="description"
                placeholder="Brief description"
                required
                value={formData.description}
                onChange={(e) => handleInputChange("description", e.target.value)}
              />
            </div>

            <div className="grid gap-2">
              <Label htmlFor="publisher-1">Publisher</Label>
              <Input
                id="publisher-1"
                name="publisher"
                placeholder="Publisher name"
                required
                value={formData.publisher}
                onChange={(e) => handleInputChange("publisher", e.target.value)}
              />
            </div>

            <div className="grid gap-2">
              <Label htmlFor="creator-1">Creator</Label>
              <Input
                id="creator-1"
                name="creator"
                placeholder="Creator name"
                required
                value={formData.creator}
                onChange={(e) => handleInputChange("creator", e.target.value)}
              />
            </div>
          </div>
          <DialogFooter>
            <DialogClose asChild>
              <Button variant="outline" type="button">
                Cancel
              </Button>
            </DialogClose>
            <Button type="submit" disabled={loading || !isFormValid}>
              {loading ? "Verifying..." : "Submit"}
            </Button>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  );
};

export default VerifyContent;
