# Chat Page - Tính năng đã hoàn thiện

## 🎨 Giao diện

### Dark/Light Mode
- ✅ Nút toggle theme ở góc phải header
- ✅ Tự động theo theme hệ thống
- ✅ Lưu preference của user

### Sidebar
- ✅ Có thể đóng/mở
- ✅ Danh sách lịch sử chat
- ✅ Nút tạo cuộc trò chuyện mới
- ✅ Nút tài khoản

## 💬 Tin nhắn

### Hiển thị tin nhắn
- ✅ User: Khung bo tròn, căn phải, màu nhẹ nhàng
- ✅ AI: Không khung, căn trái
- ✅ Avatar khác biệt cho User và AI

### Các loại tin nhắn AI có thể gửi

#### 1. Text Message
- Tin nhắn văn bản thông thường
- **Tính năng Text-to-Speech**: Hover vào tin nhắn sẽ hiện nút speaker để nghe

#### 2. Recipe Card
- Hiển thị công thức nấu ăn đẹp mắt
- Bao gồm:
  - Tên món ăn
  - Độ khó (Dễ/Trung bình/Khó)
  - Thời gian chuẩn bị
  - Số người ăn
  - Danh sách nguyên liệu
  - Các bước thực hiện

#### 3. Nutrition Info
- Hiển thị thông tin dinh dưỡng
- Bao gồm:
  - Calories (kcal)
  - Protein (g)
  - Carbs (g)
  - Fat (g)
- Có icon màu sắc cho từng loại

#### 4. Video Embed
- Embed YouTube video trực tiếp
- Responsive 16:9 ratio
- Có title và icon YouTube

## 📝 Input Area

### Tính năng nhập liệu

#### 1. Text Input
- ✅ Textarea tự động mở rộng
- ✅ Ban đầu 1 dòng, tự động tăng khi nhập nhiều
- ✅ Enter để gửi, Shift+Enter để xuống dòng
- ✅ Placeholder rõ ràng

#### 2. Image Upload
- ✅ Nút upload ảnh (icon ImagePlus)
- ✅ Preview ảnh đã chọn
- ✅ Nút xóa ảnh (X button)
- ✅ Chỉ chấp nhận file ảnh
- ✅ Hiển thị preview 128x128px

#### 3. Voice Recorder
- ✅ Nút microphone để ghi âm
- ✅ Khi đang ghi: nút đỏ nhấp nháy + hiển thị thời gian
- ✅ Click lại để dừng ghi
- ✅ Tự động xin quyền microphone
- ✅ Format: audio/webm

#### 4. Send Button
- ✅ Nút gửi bo tròn
- ✅ Disable khi không có nội dung
- ✅ Enable khi có text HOẶC ảnh

## 🔧 Components đã tạo

### `/components/chat/ImageUpload.tsx`
- Component upload và preview ảnh
- Props: `onImageSelect`, `onImageRemove`, `selectedImage`

### `/components/chat/VoiceRecorder.tsx`
- Component ghi âm giọng nói
- Props: `onRecordingComplete`
- Sử dụng MediaRecorder API

### `/components/chat/RecipeCard.tsx`
- Component hiển thị công thức nấu ăn
- Props: `title`, `ingredients`, `steps`, `prepTime`, `servings`, `difficulty`

### `/components/chat/VideoEmbed.tsx`
- Component embed YouTube video
- Props: `videoUrl`, `title`
- Tự động extract video ID từ URL

### `/components/chat/NutritionInfo.tsx`
- Component hiển thị thông tin dinh dưỡng
- Props: `calories`, `protein`, `carbs`, `fat`, `servings`

## 🎯 Cách sử dụng cho Backend

### Message Format

Backend cần trả về messages theo format:

```typescript
// Text message
{
  id: number,
  role: "user" | "assistant",
  type: "text",
  content: string
}

// Recipe message
{
  id: number,
  role: "assistant",
  type: "recipe",
  recipe: {
    title: string,
    ingredients: string[],
    steps: string[],
    prepTime?: string,
    servings?: number,
    difficulty?: "Dễ" | "Trung bình" | "Khó"
  }
}

// Nutrition message
{
  id: number,
  role: "assistant",
  type: "nutrition",
  nutrition: {
    calories?: number,
    protein?: number,
    carbs?: number,
    fat?: number,
    servings?: number
  }
}

// Video message
{
  id: number,
  role: "assistant",
  type: "video",
  video: {
    url: string,
    title?: string
  }
}
```

## 📱 Responsive
- ✅ Mobile-friendly
- ✅ Sidebar tự động collapse trên mobile
- ✅ Input area responsive
- ✅ Cards responsive

## 🚀 Chạy thử
```bash
npm run dev
```
Truy cập: `http://localhost:3000/chat`

