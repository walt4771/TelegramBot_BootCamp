import {Entity, PrimaryGeneratedColumn, Column} from "typeorm";

@Entity()
export class Book {

    @PrimaryGeneratedColumn()
    id: number;

    @Column()
    CONTENT: string;

    @Column()
    DATE: string;

}
