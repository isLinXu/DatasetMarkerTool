import os
import json
import cv2
import numpy as np
from pycocotools import mask as maskUtils

def labelme_to_coco(labelme_jsons, image_dir, output_json, output_image_dir, category_name, shape_type):
    coco_output = {
        "info": {},
        "licenses": [],
        "images": [],
        "annotations": [],
        "categories": []
    }

    category_id = 1
    annotation_id = 1
    coco_output["categories"].append({
        "id": category_id,
        "name": category_name,
        "supercategory": "none"
    })

    for image_id, labelme_json in enumerate(labelme_jsons):
        with open(labelme_json, 'r') as f:
            labelme_data = json.load(f)

        try:
            file_name = labelme_data["imagePath"]
            image_height = labelme_data["imageHeight"]
            image_width = labelme_data["imageWidth"]
        except KeyError as e:
            print(f"KeyError: {e} in file {labelme_json}")
            continue

        image_path = os.path.join(image_dir, file_name)
        if not os.path.exists(image_path):
            print(f"Image file {image_path} does not exist.")
            continue

        image_info = {
            "id": image_id,
            "file_name": file_name,
            "height": image_height,
            "width": image_width
        }
        coco_output["images"].append(image_info)

        image = cv2.imread(image_path)
        for shape in labelme_data["shapes"]:
            if shape["shape_type"] == shape_type:
                points = shape["points"]
                polygon = [p for point in points for p in point]
                segmentation = [polygon]

                mask = np.zeros((image_height, image_width), dtype=np.uint8)
                points_array = np.array(points, dtype=np.int32)
                cv2.fillPoly(mask, [points_array], 1)
                rle = maskUtils.encode(np.asfortranarray(mask))
                area = maskUtils.area(rle)
                bbox = maskUtils.toBbox(rle)

                annotation = {
                    "id": annotation_id,
                    "image_id": image_id,
                    "category_id": category_id,
                    "segmentation": segmentation,
                    "area": float(area),
                    "bbox": bbox.tolist(),
                    "iscrowd": 0
                }
                coco_output["annotations"].append(annotation)
                annotation_id += 1

                # 绘制mask区域
                color = (0, 255, 0)  # 绿色
                cv2.polylines(image, [points_array], isClosed=True, color=color, thickness=2)
                cv2.fillPoly(image, [points_array], color=color)

        # 保存绘制了mask区域的图像
        output_image_path = os.path.join(output_image_dir, file_name)
        cv2.imwrite(output_image_path, image)

    with open(output_json, 'w') as f:
        json.dump(coco_output, f, indent=4)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Convert LabelMe annotations to COCO format and draw masks on images")
    parser.add_argument("labelme_dir", help="Directory containing LabelMe JSON files")
    parser.add_argument("image_dir", help="Directory containing the corresponding images")
    parser.add_argument("output_json", help="Output COCO JSON file")
    parser.add_argument("output_image_dir", help="Directory to save images with drawn masks")
    parser.add_argument("--category_name", default="ph", help="Category name for the annotations")
    parser.add_argument("--shape_type", default="polygon", help="Shape type to filter (e.g., polygon, rectangle)")
    args = parser.parse_args()

    args.labelme_dir = '/Users/gatilin/PycharmProjects/DatasetMarkerTool/example/json'
    args.image_dir = '/Users/gatilin/PycharmProjects/DatasetMarkerTool/example/images'
    args.output_json = '/Users/gatilin/PycharmProjects/DatasetMarkerTool/example/coco.json'
    args.output_image_dir = '/Users/gatilin/PycharmProjects/DatasetMarkerTool/example/images_with_mask'
    args.category_name = 'ph'
    args.shape_type = 'polygon'

    if not os.path.exists(args.output_image_dir):
        os.makedirs(args.output_image_dir)

    labelme_jsons = [os.path.join(args.labelme_dir, f) for f in os.listdir(args.labelme_dir) if f.endswith('.json')]
    labelme_to_coco(labelme_jsons, args.image_dir, args.output_json, args.output_image_dir, args.category_name, args.shape_type)