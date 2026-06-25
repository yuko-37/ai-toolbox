class ImageAgent:
    def generate_image(self, prompt: str) -> str:
        # gpt = OpenAI()
        # response = gpt.images.generate(
        #     model="gpt-image-1-mini",
        #     prompt=f"{description}. Use {style} style.",
        #     size="1024x1024",
        #     n=1
        # )
        # image_data = base64.b64decode(response.data[0].b64_json)
        # img = Image.open(BytesIO(image_data))
        # url = f"/Users/yuko/MyFiles/dnd-images/{image_filename}.png"
        # img.save(url)
        # return url
        return "file:///Users/yuko/MyFiles/dnd-images/Elvish%20Performer.png"